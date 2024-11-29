import json
import os
from datetime import datetime
import random
from src.environment import Environment
from src.agent import Agent
from src.IndepentcheckpointAgent import IndependentCheckpointAgent
from src.visualization import Visualization
import time
from data.fire_probabilities import fire_probabilities

class Simulation:
    def __init__(self, environment, agents):
        self.environment = environment
        self.agents = agents
        self.steps = 0
        self.visualization = Visualization(environment, agents)
        self.results_folder = "simulation_results"  # Carpeta para guardar resultados
        # Variables separadas para cada tipo de agente
        self.agent_evacuated = 0
        self.agent_trapped = 0
        self.independent_checkpoint_evacuated = 0
        self.independent_checkpoint_trapped = 0
        self.fire_spread_probability = random.choice(fire_probabilities)

    def run(self, max_steps, delay):
        for step in range(max_steps):
            self.steps = step
            print(f"Step {step}")

            # Actualizar la visualización
            self.visualization.update_plot()

            # Mover agentes
            for agent in self.agents:
                if isinstance(agent, IndependentCheckpointAgent):
                    agent.move(self.environment)
                elif agent.alive:  # Otros agentes
                    agent.move(self.environment)

            # Actualizar la propagación del fuego
            
            self.environment.update_fire(self.fire_spread_probability)

            # Contar agentes evacuados y atrapados por separado
            self.agent_evacuated = sum(
                agent.position == agent.goal for agent in self.agents if isinstance(agent, Agent)
            )
            self.agent_trapped = sum(
                agent.position != agent.goal for agent in self.agents if isinstance(agent, Agent)
            )
            self.independent_checkpoint_evacuated = sum(
                agent.current_goal_index >= len(agent.checkpoints) for agent in self.agents if isinstance(agent, IndependentCheckpointAgent)
            )
            self.independent_checkpoint_trapped = sum(
                agent.current_goal_index < len(agent.checkpoints) for agent in self.agents if isinstance(agent, IndependentCheckpointAgent)
            )

            time.sleep(delay)  # Pausa para visualización

        # Mostrar estadísticas finales
        self.show_statistics()
        self.visualization.show_final()
        self.save_results()
        print("Simulation complete.")

    def show_statistics(self):
        """Muestra estadísticas finales de la simulación."""
        print("\nSimulation Statistics")
        print("---------------------")
        print (f"Fire spread probability: {self.fire_spread_probability}")
        print(f"Steps taken: {self.steps}")
        print(f"Agent (normal):")
        print(f"  Evacuated: {self.agent_evacuated}")
        print(f"  Trapped: {self.agent_trapped}")
        print(f"IndependentCheckpointAgent:")
        print(f"  Evacuated: {self.independent_checkpoint_evacuated}")
        print(f"  Trapped: {self.independent_checkpoint_trapped}")

    def save_results(self):
        """Guarda los resultados de la simulación en un archivo JSON."""
        # Crear la carpeta de resultados si no existe
        os.makedirs(self.results_folder, exist_ok=True)

        # Nombre del archivo basado en la fecha y hora actual
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.results_folder, f"simulation_{timestamp}.json")

        # Datos a guardar
        data = {
            "steps_taken": self.steps,
            "fire_spread_probability": self.fire_spread_probability,
            "breakdown_by_agent_type": {
                "Agent": {
                    "evacuated": self.agent_evacuated,
                    "trapped": self.agent_trapped
                },
                "IndependentCheckpointAgent": {
                    "evacuated": self.independent_checkpoint_evacuated,
                    "trapped": self.independent_checkpoint_trapped
                }
            }
        }

        # Escribir en el archivo JSON
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Results saved to {filename}")
