import os
from pydantic import BaseModel, Field # <--- Added this
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import JSONSearchTool

#force local mode
os.environ["OPENAI_API_KEY"] = "NA"

#defining the structure for your final output
class YelpPrediction(BaseModel):
    stars: float = Field(..., description="The predicted star rating from 1 to 5")
    review: str = Field(..., description="The synthesized review text")

@CrewBase
class MyProjectCrew():
    """MyProject crew"""

    #setting up paths
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base_path, "..", "..", "data"))

    #local RAG configuration
    rag_config = {
        "embedding_model": {
            "provider": "sentence-transformer",
            "config": {"model_name": "BAAI/bge-small-en-v1.5"}
        }
    }

    # Tools defined as class attributes
    user_tool = JSONSearchTool(
        json_path=os.path.join(data_dir, 'user_subset.json'),
        collection_name='user_data_final',
        config=rag_config
    )
    item_tool = JSONSearchTool(
        json_path=os.path.join(data_dir, 'item_subset.json'),
        collection_name='item_data_final',
        config=rag_config
    )
    review_tool = JSONSearchTool(
        json_path=os.path.join(data_dir, 'review_subset.json'),
        collection_name='review_data_final',
        config=rag_config
    )

    @agent
    def user_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['user_profiler'],
            tools=[self.user_tool, self.review_tool],
            verbose=True
        )

    @agent
    def item_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['item_analyst'],
            tools=[self.item_tool, self.review_tool],
            verbose=True
        )

    @agent
    def prediction_modeler(self) -> Agent:
        return Agent(
            config=self.agents_config['prediction_modeler'],
            verbose=True
        )

    @task
    def analyze_user_task(self) -> Task:
        return Task(config=self.tasks_config['analyze_user_task'])

    @task
    def analyze_item_task(self) -> Task:
        return Task(config=self.tasks_config['analyze_item_task'])

    @task
    def predict_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['predict_review_task'],
            output_pydantic=YelpPrediction # <--- Changed output_json to output_pydantic
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )