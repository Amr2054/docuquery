from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    # This function solves the clash between async and normal function when calling
    # __init__ and init_collection so using this function we can safely call both
    @classmethod
    async def create_instance(cls,db_client: object):
        instance = cls(db_client=db_client) # creates an object of ProjectModel
        await instance.init_collection()
        return instance

    # check on all collections and initialize indexes within collection
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name = index["name"],
                    unique = index["unique"],
                )

# function should be async cause motor uses async functions and we can use await
    async def create_project(self, project: Project):
        # inserting a new project (as dict) in project collection inside DB
        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id

        return project

    async def get_project_or_create_one(self,project_id:str):
        # we are searching a project_id field that equals project_id
        record = await self.collection.find_one({ # return a dict.
            "project_id": project_id
        })

        if record is None:
            # create new project
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)

            return project

        return Project(**record)

    async def get_all_projects(self, page: int=1, page_size: int=10):

        # count total number of documents
        total_documents = await self.collection.count_documents({})

        total_pages = total_documents // page_size
        if total_documents % page_size > 0 :
            total_pages += 1

        cursor = self.collection.find().skip( (page-1) * page_size ).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(
                Project(**document)
            )

        return projects, total_pages