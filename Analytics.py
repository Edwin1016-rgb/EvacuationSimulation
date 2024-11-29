import os
import json
import matplotlib.pyplot as plt

class Analytics:
    def __init__(self, results_folder="dist/simulation_results"):
        self.results_folder = results_folder
        self.data = []
        self.summary = {
            "Agent": {"evacuated": 0, "trapped": 0, "count": 0},
            "IndependentCheckpointAgent": {"evacuated": 0, "trapped": 0, "count": 0},
        }

    def load_data(self):
        """Carga todos los archivos JSON de la carpeta especificada."""
        if not os.path.exists(self.results_folder):
            print(f"La carpeta '{self.results_folder}' no existe.")
            return

        for filename in os.listdir(self.results_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(self.results_folder, filename)
                with open(file_path, "r") as file:
                    simulation_data = json.load(file)
                    self.data.append(simulation_data)

    def analyze(self):
        """Procesa los datos cargados para calcular promedios."""
        for sim in self.data:
            for agent_type, stats in sim["breakdown_by_agent_type"].items():
                self.summary[agent_type]["evacuated"] += stats["evacuated"]
                self.summary[agent_type]["trapped"] += stats["trapped"]
                self.summary[agent_type]["count"] += 1

        # Calcular promedios
        for agent_type, stats in self.summary.items():
            if stats["count"] > 0:
                stats["avg_evacuated"] = stats["evacuated"] / stats["count"]
                stats["avg_trapped"] = stats["trapped"] / stats["count"]
            else:
                stats["avg_evacuated"] = 0
                stats["avg_trapped"] = 0

    def plot_results(self):
        """Genera una gráfica comparativa de los resultados analizados."""
        agent_types = list(self.summary.keys())
        avg_evacuated = [self.summary[agent]["avg_evacuated"] for agent in agent_types]
        avg_trapped = [self.summary[agent]["avg_trapped"] for agent in agent_types]

        x = range(len(agent_types))
        plt.bar(x, avg_evacuated, width=0.4, label="Evacuated", color="green", align="center")
        plt.bar(x, avg_trapped, width=0.4, label="Trapped", color="red", align="edge")
        plt.xticks(x, agent_types)
        plt.ylabel("Average Count")
        plt.title("Average Evacuation and Trapped by Agent Type")
        plt.legend()
        plt.show()

    def run(self):
        """Carga los datos, los analiza y muestra la gráfica."""
        self.load_data()
        self.analyze()
        self.plot_results()
        
if __name__ == "__main__":
    analytics = Analytics(results_folder="simulation_results")
    analytics.run()