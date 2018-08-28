Point Based MultiAgent Visual Environment
=========================================
This project is a visual tool for visualizing and simulating multiagent systems
in a point based environment. This can be integrated onto existing projects for
testing purposes and for providing a visual aid.

## How can I use this?
Easy peasy. Just include this repository into your project. You can either:
 - Clone it into your project.
   ```bash
   git clone https://github.com/aarg-kcis/PointEnvironment.git
   ```
 - Add it as a submodule in your repository.
   ```bash
   git submodule add https://github.com/aarg-kcis/PointEnvironment.git
   git submodule update --init --recursive
   ```

## Jump Start
To integrate it in your existing code follow these steps:
 - Create an PointEnvironment instance
   ```python
   from PointEnvironment.Environment import PointEnvironment
   from PointEnvironment.Agent import Agent
   from PointEnvironment.Pose import Pose
   visualOptions = { 'tailLength' : 4, # tail of agent's trajectory
                     'speedup' : 1, # realTime/simTime
                     'bounds': [-10,10,-10,10]# bounds of the environment [xmin, xmax, ymin, ymax]
                     }
   options = { 'num_iterations' : 50, # no. of steps environment takes for one step call
               'dt' : 0.01, # dt in in kinametic update
               'visualize' : True, # show visualization?
               'visualOptions' : visualOptions # visual options
               }

   env = PointEnvironment(**options)
   ```
 - Add some agents to the environment
   ```python
   # Add some agents to the environment
   env.addAgent(Agent(0, Pose(0,0,0)))
   env.addAgent(Agent(1, Pose(1,0,0)))
 - Start the visualizer
   ```python
   # start the visualiser
   env.startVisualiser()
   ```
 - Provide some velocities to the agents
   ```python
   # give some actions to the agents through environment instance
   # some random loop
   for i in range(100):
     # This is the method to call...
     # step takes a dict containing agent id and respective values for action [v, w]
     env.step({k:[0.4*(k+1), 0.2*(k+1)] for k in range(2)})
     # step method takes a dict as input for the following form:
     # {agent_id : [linear_velocity, angular_velocity]}
   ```
 Agents in environment which are'nt mentioned in the dictionary passed to the step method are not moved

## Classes
#### Pose:
Stores the pose information of the agents and has methods to update them accordingly.

Attributes:
 - **x** <`float`>: x coordinate
 - **y** <`float`>: y coordinate
 - **theta** <`float`>: Heading in radians
```python
# Pose(x, y, theta(in radians))
some_random_pose = Pose(0, 1, 2)
```

#### Agent:
Atrributes:
- **id** <`int`>: ID of the agent. This has to be unique in an environment
- **pose** <`Pose`>: Initial pose of the agent. (def: None corresponds to Pose(0,0,0))
- **defaultPose** <`Pose`>: The agent will return to this pose when the environment is reset. (def: pose specified in pose)
- **collisionRadius** <`float`>: The collision radius of the agent in meters. (def 0.15)
```python
some_agent = Agent(0, some_random_pose)
```

#### Visualizer:
Attributes:
 - **tailLength** <`int`>: # of poses to plot per agent. (def: 5)
 - **speedup** <`int`>: Ratio of realTime over simTime. (def: 1)
 - **bounds** <`list`>: Bounds odf the environment. Currently it should be given. (def: None)

#### PointEnvironment
Attributes:
 - **num_iterations** <`int`>: # of steps environment takes for one step call. (def: 100)
 - **dt** <`float`>: dt to use in in kinametic update. (def: 1e-2)
 - **agents** <`[Agents]`>: List of agents to add in environment. Agents can be added later by addAgent method. (def: None)
 - **visualize** <`bool`>: Show visualization?
 - **visualOptions** <`dict`>: Refer to attributes of Visualizer class. Should be given only when `visualize == True`
 ```python
 # Adding agents via constructor call
 some_env = env(agents=[some_agent])
 # Oops.. forgot to add an agent?
 # Don't worry
 some_env.addAgent(Agent(1, some_random_pose))
 # **dabs**
 ```

Methods:
 - **step**:
 Steps the environment. All agents perform actions specified in the argument. If an action is'nt provided for an agent it does'nt perform any.

  args-> `dict` of the following form:
 ```python
 # {agent_id: action for agent whith this id}
 actions_for_agents = [[0.4, 0.3], [0.4, 0]]
 agent_actions = {i[0]:i[1] for i in enumerate(actions_for_agents)}
 some_env.step(agent_actions)
 ```
 - **reset**: Resets the environment and returns agents to the poses provided in the argument. If a pose is'nt provided for an agent it resets to its `defaultPose`

  args-> *(optional)* `dict` of Pose of the following form
 ```python
 # {agent_id: pose for agent whith this id}
 some_poses_in_dict = {0, Pose(0,0,1)}
 some_env.reset(some_poses_in_dict)

 ```
 - **addAgents**:
 Adds agents provided as arguments to the environment.

  args-> `list` of `Agent` instances
 ```python
 some_agents_in_list = [Agent(2, Pose(2,2,2)), Agent(3, Pose(4,5,6))]
 some_env.addAgents(some_agents_in_list)

 ```
  - **addAgent**:
 Adds agents provided as arguments to the environment.

  args-> `Agent` instance
 ```python
 some_env.addAgents(Agent(4, Pose()))

 ```
 - **startVisualiser**
 Starts the visualizer thread.
  ```python
 env.startVisualiser()
 ```
