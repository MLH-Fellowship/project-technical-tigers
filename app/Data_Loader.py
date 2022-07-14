import json

class Data_Loader:
    def __init__(self):
        self.landing_page_data = self.get_data_from_json('app/data/landingPage.json')
        self.about_me_data = self.get_data_from_json('app/data/aboutMe.json')
        self.projects_data = self.get_data_from_json('app/data/projects.json')
        self.expiriences_data = self.get_data_from_json('app/data/expiriences.json')
        self.skills_data = self.get_data_from_json('app/data/skills.json')

    def get_data_from_json(self, file_path):
        with open(file_path) as file:
            data = json.load(file)
        return data