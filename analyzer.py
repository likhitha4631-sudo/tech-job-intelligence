class MarketAnalyzer:

    def __init__(self, skills_list):
        self.skills_list = skills_list
        self.skill_count = {}
        self.experience_skill_count = {}
        self.salary_skill_map = {}

    def analyze(self, job_data):

        self.skill_count = {}
        self.experience_skill_count = {}
        self.salary_skill_map = {}

        for row in job_data:

            description = (row.get("description") or "").lower()
            experience = row.get("experience") or "Unknown"
            salary = row.get("salary") or 0

            try:
                salary = int(salary)
            except:
                salary = 0

            for skill in self.skills_list:
                if skill.lower() in description:

                    # Overall skill count
                    self.skill_count[skill] = self.skill_count.get(skill, 0) + 1

                    # Experience-wise count
                    if experience not in self.experience_skill_count:
                        self.experience_skill_count[experience] = {}

                    self.experience_skill_count[experience][skill] = \
                        self.experience_skill_count[experience].get(skill, 0) + 1

                    # Salary tracking
                    if skill not in self.salary_skill_map:
                        self.salary_skill_map[skill] = []

                    self.salary_skill_map[skill].append(salary)

    def get_top_skills(self, top_n=5):
        return sorted(
            self.skill_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

    def get_experience_analysis(self):
        return self.experience_skill_count

    def get_average_salary_by_skill(self):
        avg_salary = {}

        for skill, salaries in self.salary_skill_map.items():
            if salaries:
                avg_salary[skill] = sum(salaries) / len(salaries)

        return avg_salary