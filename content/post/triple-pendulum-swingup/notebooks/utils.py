def CartMultiPendulumSystem(m_cart=1, m1=1, l1=1, **kwargs):
    """A system representing a cart with serial connected pendulum bars

    Args:
        m_cart: mass of the cart in kg
        m1: mass of pendulum #1 in kg
        l1: length of pendulum #1 in kg
        m2, l2, ...

    Returns:
        Diagram: get_input_port(0) is the force to the cart
                 get_output_port(0) is the state of the system, length==2*(N+1) where N is the number of pendulums
                 get_output_port(1) is the query output port of the scene graph
    """
    from pydrake.all import (
        AddMultibodyPlantSceneGraph,
        DiagramBuilder,
        Parser,
    )

    kwargs['m1'] = m1
    kwargs['l1'] = l1
    sdf_string, num_pendulums = _CartMultiPendulumSdf(m_cart, **kwargs)

    builder = DiagramBuilder()
    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.0)
    Parser(plant, scene_graph).AddModelsFromString(sdf_string, "sdf")
    plant.Finalize()

    builder.ExportInput(plant.GetInputPort("cart_multi_pendulum_actuation"), "f_cart")
    builder.ExportOutput(plant.GetOutputPort("cart_multi_pendulum_state"), "x")
    builder.ExportOutput(scene_graph.get_query_output_port(), "query")

    cart_multi_pendulum = builder.Build()

    numerals = {1:'Single', 2:'Double', 3:'Triple', 4:'Quadruple', 5: 'Quintuple', 6: 'Sextuple'}
    plant.set_name(f"Cart{numerals[num_pendulums]}Pendulum" if num_pendulums in numerals else f"Cart{num_pendulums}Pendulum")

    return cart_multi_pendulum


def _CartMultiPendulumSdf(m_cart, **kwargs):
    from matplotlib.colors import LinearSegmentedColormap

    num_pendulums = 0
    while len(kwargs) != num_pendulums * 2:
        num_pendulums += 1
        if f'm{num_pendulums}' not in kwargs:
            raise RuntimeError(f" Missing argument 'm{num_pendulums}'")
        if f'l{num_pendulums}' not in kwargs:
            raise RuntimeError(f" Missing argument 'l{num_pendulums}'")

    sdf_string = f"""
    <link name="cart">
        <pose>0 0 0 0 0 0</pose>
        <inertial>
            <mass>{m_cart}</mass>
        </inertial>
        <visual name="cart_body">
            <geometry>
                <box>
                    <size>0.5 0.3 0.3</size>
                </box>
            </geometry>
            <material>
            <diffuse>0.5 0.5 0.5 1</diffuse>
            </material>
        </visual>
        <visual name="cart_wheel1">
            <pose>-0.15 0 -0.2 1.57 0 0</pose>
            <geometry>
                <cylinder>
                    <radius>0.05</radius>
                    <length>0.3</length>
                </cylinder>
            </geometry>
            <material>
                <diffuse>0 0 0 1</diffuse>
            </material>
        </visual>
        <visual name="cart_wheel2">
            <pose>0.15 0 -0.2 1.57 0 0</pose>
            <geometry>
                <cylinder>
                    <radius>0.05</radius>
                    <length>0.3</length>
                </cylinder>
            </geometry>
            <material>
                <diffuse>0 0 0 1</diffuse>
            </material>
        </visual>
    </link>

    <joint name="linear" type="prismatic">
        <parent>world</parent>
        <child>cart</child>
        <axis>
            <xyz>1 0 0</xyz>
        </axis>
    </joint>
    """

    # colormap interpolating red -> green -> blue
    cmap = LinearSegmentedColormap.from_list("red_green_blue", [(1,0,0), (0,1,0), (0,0,1)])

    # parent_link and z for each joint, update each iteration
    parent_link = 'cart'
    y = -0.17
    z = 0.0
    for i in range(1,num_pendulums+1):
        mi = kwargs[f'm{i}']
        li = kwargs[f'l{i}']
        rod_radius = 0.02

        color = cmap((i-1) / (num_pendulums-1)) if num_pendulums > 1 else cmap(1)

        sdf_string += f"""
        <link name="pendulum{i}">
            <pose>0 {y} {z} 0 0 0</pose>
            <inertial>
                <pose>0 0 {-li/2} 0 0 0</pose>
                <mass>{mi}</mass>
                <inertia>
                    <ixx>{mi * li**2 / 12}</ixx>
                    <iyy>{mi * li**2 / 12}</iyy>
                    <izz>{mi * rod_radius**2 / 2}</izz>
                </inertia>
            </inertial>
            <visual name="pendulum{i}_rod">
                <pose>0 0 {-li/2} 0 0 0</pose>
                <geometry>
                    <cylinder>
                        <radius>{rod_radius}</radius>
                        <length>{li}</length>
                    </cylinder>
                </geometry>
                <material>
                    <diffuse>{' '.join([str(c) for c in color])}</diffuse>
                </material>
            </visual>
        </link>
        <joint name="joint{i}" type="continuous">
            <parent>{parent_link}</parent>
            <child>pendulum{i}</child>
            <axis>
                <xyz>0 -1 0</xyz>
                <limit>
                    <effort>0</effort>
                </limit>
            </axis>
        </joint>
        """
        y -= 2 * rod_radius
        z -= li
        parent_link = f'pendulum{i}'

    sdf_string = f"""
    <?xml version="1.0" ?>
    <sdf version="1.7">
        <model name="cart_multi_pendulum">
            {sdf_string}
            <link name="ground">
                <visual name="ground_rail">
                    <pose>0 0 -0.3 0 0 0</pose>
                    <geometry>
                        <box>
                            <size>50 0.3 0.1</size>
                        </box>
                    </geometry>
                    <material>
                        <diffuse>0.9 0.9 0.9 1</diffuse>
                    </material>
                </visual>
                <visual name="ground_origin">
                    <pose>0 0 -0.3 0 0 0</pose>
                    <geometry>
                        <box>
                            <size>0.01 0.301 0.1</size>
                        </box>
                    </geometry>
                    <material>
                        <diffuse>0 0 0 1</diffuse>
                    </material>
              </visual>
            </link>
            <joint name="ground_fixed" type="fixed">
                <parent>world</parent>
                <child>ground</child>
            </joint>
        </model>
    </sdf>
    """
    return sdf_string, num_pendulums