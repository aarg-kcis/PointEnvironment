
PROVIDE_SHAPE_INSTANCE = "shape should be an instance of <class Shape>"
DESCRIPTION_INVALID = "Error in generating description from JSON"
N_STATES_MISMATCH = "Number of state entries must be equal to N_AGENTS C 2"
NOT_UNIT_VEC = "Please make sure the vector is unit"
TYPE_MISMATCH = lambda a,b: "TYPE MISMATCH: Expected {} and got {}".format(b, a.__class__)
AGENT_NOT_UNIQUE = lambda a: "Multiple agents with the same id [{}]".format(a.id)
ACTION_MISSING = lambda a: "No action found for Agent[{}].".format(a)
ACTION_MISSING = lambda a: "No reset pose specified for Agent[{0}].\nResetting Agent[{0}] to default pose".format(a)
BAD_RESET_POSE = lambda a: "Bad reset pose specified. Expected pose to be instance of Pose or False for default, got {}".format(type(a))
CANT_ADD_POSE = lambda a: "Provide either pose or mat/arr of shape (1,3). Got {} instead".format(a)
RESET_POSE_MISSING = lambda a: "Reset pose missing for Agent[{0}].\nResetting Agent[{0}] to default pose".format(a)
COLLISION = lambda a,b : "Collision b/w Agent[{}] & Agent[{}]".format(a,b)