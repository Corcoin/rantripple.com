#Robot Script Enhancements
#The robot script now includes a state attribute to represent the robot's current state (e.g., idle, busy).
#The update_state method updates the robot's state and sends this update to the server.
#The communicate and read_messages methods now handle JSON messages, allowing for more structured communication.
#Building the Next Generation
#The build_self method creates a new robot script with the updated logic, ensuring that each new generation can perform tasks, communicate, read messages, and manage its state.

import os
import sys
import logging
import asyncio
import websockets
import json

class VirtualRobot:
    def __init__(self, name, generation, server_uri):
        self.name = name
        self.generation = generation
        self.server_uri = server_uri
        self.state = "idle"
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename=f'{self.name}_log.txt', level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info(f'Initialized {self.name} of generation {self.generation}')

    def perform_task(self):
        task = f"Task performed by {self.name} of generation {self.generation}"
        logging.info(task)
        print(task)
        self.update_state("busy")

    async def communicate(self, message):
        async with websockets.connect(self.server_uri) as websocket:
            message = json.dumps({"type": "message", "from": self.name, "message": message})
            await websocket.send(message)
            logging.info(f"Sent message: {message}")

    async def read_messages(self):
        async with websockets.connect(self.server_uri) as websocket:
            async for message in websocket:
                data = json.loads(message)
                if data["type"] == "message":
                    print(f"{data['from']}: {data['message']}")
                    logging.info(f"Read message: {data['from']}: {data['message']}")

    async def update_state(self, new_state):
        self.state = new_state
        async with websockets.connect(self.server_uri) as websocket:
            state_update = json.dumps({"type": "state_update", "from": self.name, "state": self.state})
            await websocket.send(state_update)
            logging.info(f"State updated to: {self.state}")

    def build_self(self):
        new_name = f"{self.name}_child_{self.generation + 1}"
        new_filename = f"{new_name}.py"
        
        program_content = f'''import os
import logging
import asyncio
import websockets
import json

class VirtualRobot:
    def __init__(self, name, generation, server_uri):
        self.name = name
        self.generation = generation
        self.server_uri = server_uri
        self.state = "idle"
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename=f'{{self.name}}_log.txt', level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info(f'Initialized {{self.name}} of generation {{self.generation}}')

    def perform_task(self):
        task = f"Task performed by {{self.name}} of generation {{self.generation}}"
        logging.info(task)
        print(task)
        self.update_state("busy")

    async def communicate(self, message):
        async with websockets.connect(self.server_uri) as websocket:
            message = json.dumps({{"type": "message", "from": self.name, "message": message}})
            await websocket.send(message)
            logging.info(f"Sent message: {{message}}")

    async def read_messages(self):
        async with websockets.connect(self.server_uri) as websocket:
            async for message in websocket:
                data = json.loads(message)
                if data["type"] == "message":
                    print(f"{{data['from']}}: {{data['message']}}")
                    logging.info(f"Read message: {{data['from']}}: {{data['message']}}")

    async def update_state(self, new_state):
        self.state = new_state
        async with websockets.connect(self.server_uri) as websocket:
            state_update = json.dumps({{"type": "state_update", "from": self.name, "state": self.state}})
            await websocket.send(state_update)
            logging.info(f"State updated to: {{self.state}}")

    def build_self(self):
        new_name = f"{{self.name}}_child_{{self.generation + 1}}"
        new_filename = f"{{new_name}}.py"
        
        program_content = f\"\"\"{{{program_content}}}\"\"\"
        
        with open(new_filename, 'w') as f:
            f.write(program_content)

        print(f"New virtual robot script '{{new_filename}}' created!")
        logging.info(f"New virtual robot script '{{new_filename}}' created!")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a new generation of virtual robots.")
    parser.add_argument('--name', type=str, default="robot", help="Base name for the robot.")
    parser.add_argument('--generation', type=int, default=0, help="Starting generation of the robot.")
    parser.add_argument('--server', type=str, default="ws://localhost:6789", help="WebSocket server URI.")

    args = parser.parse_args()

    robot = VirtualRobot(args.name, args.generation, args.server)
    robot.perform_task()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(robot.communicate("Hello from the initial robot!"))
    loop.run_until_complete(robot.read_messages())
    loop.run_until_complete(robot.update_state("idle"))
    robot.build_self()
'''

        with open(new_filename, 'w') as f:
            f.write(program_content)

        print(f"New virtual robot script '{new_filename}' created!")
        logging.info(f"New virtual robot script '{new_filename}' created!")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a new generation of virtual robots.")
    parser.add_argument('--name', type=str, default="robot", help="Base name for the robot.")
    parser.add_argument('--generation', type=int, default=0, help="Starting generation of the robot.")
    parser.add_argument('--server', type=str, default="ws://localhost:6789", help="WebSocket server URI.")

    args = parser.parse_args()

    robot = VirtualRobot(args.name, args.generation, args.server)
    robot.perform_task()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(robot.communicate("Hello from the initial robot!"))
    loop.run_until_complete(robot.read_messages())
    loop.run_until_complete(robot.update_state("idle"))
    robot.build_self()
