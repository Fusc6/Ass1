from abc import ABC, abstractmethod
from copy import deepcopy

# ----------------------------------
# Base Classes
# ----------------------------------

class Component(ABC):
    """
    Abstract base class for all components.
    Defines the interface for display_string, to_csv, parse_csv, make_copy, and __eq__.
    """

    def __init__(self, name: str, price: float):
        self.name = name               # e.g. "Wire", "Battery", "Sensor", ...
        self.price = float(price)      # dollars and cents

    @abstractmethod
    def display_string(self) -> str:
        """Return a user-friendly display string (no quantity)."""
        pass

    @abstractmethod
    def to_csv(self) -> str:
        """Return a comma-separated string of this component's data (excluding quantity)."""
        pass

    @abstractmethod
    def make_copy(self):
        """Return a deep copy (or equivalent) of this component."""
        pass

    @staticmethod
    @abstractmethod
    def parse_csv(values: list):
        """
        Parse a list of CSV values (which do NOT include quantity as the first field)
        and return an instance of the appropriate Component subclass.
        """
        pass

    def __eq__(self, other) -> bool:
        """Compare two components for equality based on their attributes."""
        if not isinstance(other, Component):
            return False
        return (
            self.name == other.name
            and abs(self.price - other.price) < 1e-9  # float comparison
        )

    def __str__(self):
        """Alias for the display string."""
        return self.display_string()


# ----------------------------------
# Concrete Component Classes
# ----------------------------------

class Wire(Component):
    """
    Wires have:
      - length (mm)
      - price
      - name (always "Wire")
    """
    def __init__(self, length: float, price: float, name="Wire"):
        super().__init__(name, price)
        self.length = float(length)

    def display_string(self) -> str:
        # Example: "40mm Wire $2.40"
        return f"{self.length:.0f}mm {self.name} ${self.price:.2f}"

    def to_csv(self) -> str:
        # Example: "Wire,40,2.4"
        return f"{self.name},{self.length},{self.price:.2f}"

    def make_copy(self):
        return Wire(self.length, self.price, self.name)

    @staticmethod
    def parse_csv(values: list):
        """
        Expecting values = [ 'Wire', length, price ]
        Example: ["Wire", "40", "2.4"]
        """
        # name = values[0] -> "Wire"
        length = float(values[1])
        price = float(values[2])
        return Wire(length, price, values[0])

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not isinstance(other, Wire):
            return False
        return abs(self.length - other.length) < 1e-9


class Battery(Component):
    """
    Batteries have:
      - size (AA, AAA, C, D, E)
      - voltage (V)
      - price
      - name (always "Battery")
    """
    def __init__(self, size: str, voltage: float, price: float, name="Battery"):
        super().__init__(name, price)
        self.size = size
        self.voltage = float(voltage)

    def display_string(self) -> str:
        # Example: "1.5V AA Battery $3.10"
        return f"{self.voltage:.1f}V {self.size} {self.name} ${self.price:.2f}"

    def to_csv(self) -> str:
        # Example: "Battery,AA,1.5,3.1"
        return f"{self.name},{self.size},{self.voltage},{self.price:.2f}"

    def make_copy(self):
        return Battery(self.size, self.voltage, self.price, self.name)

    @staticmethod
    def parse_csv(values: list):
        """
        Expecting values = [ 'Battery', size, voltage, price ]
        Example: ["Battery", "AA", "1.5", "3.1"]
        """
        size = values[1]
        voltage = float(values[2])
        price = float(values[3])
        return Battery(size, voltage, price, values[0])

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not isinstance(other, Battery):
            return False
        return (
            self.size == other.size and
            abs(self.voltage - other.voltage) < 1e-9
        )


class SolarPanel(Component):
    """
    Solar Panels have:
      - voltage (V)
      - current (mA)
      - price
      - name (always "Solar Panel")
      - can calculate wattage (voltage * current / 1000)
    """
    def __init__(self, voltage: float, current: float, price: float, name="Solar Panel"):
        super().__init__(name, price)
        self.voltage = float(voltage)
        self.current = float(current)

    def calc_wattage(self) -> float:
        """Returns wattage in W = voltage * current / 1000 if current is in mA."""
        return self.voltage * (self.current / 1000.0)

    def display_string(self) -> str:
        # Example: "1.4V 0.4mA Solar Panel $14.00"
        return f"{self.voltage:.1f}V {self.current:.1f}mA {self.name} ${self.price:.2f}"

    def to_csv(self) -> str:
        # Example: "Solar Panel,1.4,0.4,14.00"
        return f"{self.name},{self.voltage},{self.current},{self.price:.2f}"

    def make_copy(self):
        return SolarPanel(self.voltage, self.current, self.price, self.name)

    @staticmethod
    def parse_csv(values: list):
        """
        Expecting values = [ 'Solar Panel', voltage, current, price ]
        Example: ["Solar Panel", "1.4", "0.4", "14.00"]
        """
        voltage = float(values[1])
        current = float(values[2])
        price = float(values[3])
        return SolarPanel(voltage, current, price, values[0])

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not isinstance(other, SolarPanel):
            return False
        return (
            abs(self.voltage - other.voltage) < 1e-9 and
            abs(self.current - other.current) < 1e-9
        )


class Switch(Component):
    """
    Switches have:
      - type (push, slide, rocker, toggle)
      - voltage (V)
      - price
      - name (always "Switch")
    """
    def __init__(self, switch_type: str, voltage: float, price: float, name="Switch"):
        super().__init__(name, price)
        self.switch_type = switch_type
        self.voltage = float(voltage)

    def display_string(self) -> str:
        # Example: "4.5V Push Switch $4.60"
        return f"{self.voltage:.1f}V {self.switch_type.capitalize()} {self.name} ${self.price:.2f}"

    def to_csv(self) -> str:
        # Example: "Switch,push,4.5,4.6"
        return f"{self.name},{self.switch_type},{self.voltage},{self.price:.2f}"

    def make_copy(self):
        return Switch(self.switch_type, self.voltage, self.price, self.name)

    @staticmethod
    def parse_csv(values: list):
        """
        Expecting values = [ 'Switch', switch_type, voltage, price ]
        Example: ["Switch", "push", "4.5", "4.6"]
        """
        switch_type = values[1]
        voltage = float(values[2])
        price = float(values[3])
        return Switch(switch_type, voltage, price, values[0])

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not isinstance(other, Switch):
            return False
        return (
            self.switch_type == other.switch_type and
            abs(self.voltage - other.voltage) < 1e-9
        )


class Sensor(Component):
    """
    Sensors have:
      - sensor type (motion, infrared, light, temperature, humidity, sound, dust, etc.)
      - voltage (V)
      - price
      - name (always "Sensor")
    """
    def __init__(self, sensor_type: str, voltage: float, price: float, name="Sensor"):
        super().__init__(name, price)
        self.sensor_type = sensor_type
        self.voltage = float(voltage)

    def display_string(self) -> str:
        # Example: "5.0V Motion Sensor $3.90"
        return f"{self.voltage:.1f}V {self.sensor_type.capitalize()} {self.name} ${self.price:.2f}"

    def to_csv(self) -> str:
        # Example: "Sensor,motion,5,3.9"
        return f"{self.name},{self.sensor_type},{self.voltage},{self.price:.2f}"

    def make_copy(self):
        return Sensor(self.sensor_type, self.voltage, self.price, self.name)

    @staticmethod
    def parse_csv(values: list):
        """
        Expecting values = [ 'Sensor', sensor_type, voltage, price ]
        Example: ["Sensor", "motion", "5", "3.9"]
        """
        sensor_type = values[1]
        voltage = float(values[2])
        price = float(values[3])
        return Sensor(sensor_type, voltage, price, values[0])

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not isinstance(other, Sensor):
            return False
        return (
            self.sensor_type == other.sensor_type and
            abs(self.voltage - other.voltage) < 1e-9
        )


class Light(Component, ABC):
    """
    Abstract base for all Lights (LED or Light Globe).
    Lights have:
      - colour
      - voltage (V)
      - current (mA)
      - price
      - name
      - can calculate wattage
    """

    def __init__(self, colour: str, voltage: float, current: float, price: float, name: str):
        super().__init__(name, price)
        self.colour = colour
        self.voltage = float(voltage)
        self.current = float(current)

    def calc_wattage(self) -> float:
        """Returns wattage in W = voltage * current / 1000 if current is in mA."""
        return self.voltage * (self.current / 1000.0)

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not isinstance(other, Light):
            return False
        return (
            self.colour == other.colour and
            abs(self.voltage - other.voltage) < 1e-9 and
            abs(self.current - other.current) < 1e-9
        )


class LEDLight(Light):
    """
    LED lights have:
      - colour (white, red, green, blue, yellow, orange, pink, aqua, violet)
      - voltage
      - current
      - price
      - name (always "LED Light")
    """

    def __init__(self, colour: str, voltage: float, current: float, price: float, name="LED Light"):
        super().__init__(colour, voltage, current, price, name)

    def display_string(self) -> str:
        # Example: "3.0V 150.0mA Red LED Light $2.20"
        return f"{self.voltage:.1f}V {self.current:.1f}mA {self.colour.capitalize()} {self.name} ${self.price:.2f}"

    def to_csv(self) -> str:
        # Example: "LED Light,red,3,150,2.2"
        return f"{self.name},{self.colour},{self.voltage},{self.current},{self.price:.2f}"

    def make_copy(self):
        return LEDLight(self.colour, self.voltage, self.current, self.price, self.name)

    @staticmethod
    def parse_csv(values: list):
        """
        Expecting values = [ 'LED Light', colour, voltage, current, price ]
        Example: ["LED Light", "red", "3", "150", "2.2"]
        """
        colour = values[1]
        voltage = float(values[2])
        current = float(values[3])
        price = float(values[4])
        return LEDLight(colour, voltage, current, price, values[0])


class LightGlobe(Light):
    """
    Light Globes have:
      - colour (warm, cool, neutral, etc.)
      - voltage
      - current
      - price
      - name (always "Light Globe")
    """

    def __init__(self, colour: str, voltage: float, current: float, price: float, name="Light Globe"):
        super().__init__(colour, voltage, current, price, name)

    def display_string(self) -> str:
        # Example: "6.5V 240.0mA Warm Light Globe $3.50"
        return f"{self.voltage:.1f}V {self.current:.1f}mA {self.colour.capitalize()} {self.name} ${self.price:.2f}"

    def to_csv(self) -> str:
        # Example: "Light Globe,warm,6.5,240,3.5"
        return f"{self.name},{self.colour},{self.voltage},{self.current},{self.price:.2f}"

    def make_copy(self):
        return LightGlobe(self.colour, self.voltage, self.current, self.price, self.name)

    @staticmethod
    def parse_csv(values: list):
        """
        Expecting values = [ 'Light Globe', colour, voltage, current, price ]
        Example: ["Light Globe", "warm", "6.5", "240", "3.5"]
        """
        colour = values[1]
        voltage = float(values[2])
        current = float(values[3])
        price = float(values[4])
        return LightGlobe(colour, voltage, current, price, values[0])


class Buzzer(Component):
    """
    Buzzers have:
      - frequency (Hz)
      - sound pressure (dB)
      - voltage (V)
      - current (mA)
      - price
      - name (always "Buzzer")
      - can calculate wattage
    """

    def __init__(self, frequency: float, sound_pressure: float, voltage: float,
                 current: float, price: float, name="Buzzer"):
        super().__init__(name, price)
        self.frequency = float(frequency)
        self.sound_pressure = float(sound_pressure)
        self.voltage = float(voltage)
        self.current = float(current)

    def calc_wattage(self) -> float:
        """Returns wattage in W = voltage * current / 1000 if current is in mA."""
        return self.voltage * (self.current / 1000.0)

    def display_string(self) -> str:
        # Example: "4.0V 120.0mA 240.0Hz 90dB Buzzer $5.60"
        return (f"{self.voltage:.1f}V {self.current:.1f}mA "
                f"{self.frequency:.1f}Hz {self.sound_pressure:.0f}dB {self.name} ${self.price:.2f}")

    def to_csv(self) -> str:
        # Example: "Buzzer,240,90,4,120,5.6"
        return f"{self.name},{self.frequency},{self.sound_pressure},{self.voltage},{self.current},{self.price:.2f}"

    def make_copy(self):
        return Buzzer(self.frequency, self.sound_pressure, self.voltage, self.current, self.price, self.name)

    @staticmethod
    def parse_csv(values: list):
        """
        Expecting values = [ 'Buzzer', frequency, sound_pressure, voltage, current, price ]
        Example: ["Buzzer", "240", "90", "4", "120", "5.6"]
        """
        frequency = float(values[1])
        sound_pressure = float(values[2])
        voltage = float(values[3])
        current = float(values[4])
        price = float(values[5])
        return Buzzer(frequency, sound_pressure, voltage, current, price, values[0])

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        if not isinstance(other, Buzzer):
            return False
        return (
            abs(self.frequency - other.frequency) < 1e-9 and
            abs(self.sound_pressure - other.sound_pressure) < 1e-9 and
            abs(self.voltage - other.voltage) < 1e-9 and
            abs(self.current - other.current) < 1e-9
        )


# ----------------------------------
# Component Factory for Parsing
# ----------------------------------

def parse_single_component_from_csv(quantity: int, values: list):
    """
    Given a quantity and a list of strings that describe a component,
    return (quantity, component_object).
    
    E.g. quantity=17, values=["Wire","40","2.4"]
    """
    if not values:
        return None

    comp_type = values[0].lower()  # "wire", "battery", etc.

    # Dispatch to the correct parse method based on the name:
    if comp_type == "wire":
        component = Wire.parse_csv(values)
    elif comp_type == "battery":
        component = Battery.parse_csv(values)
    elif comp_type == "solar panel":
        component = SolarPanel.parse_csv(values)
    elif comp_type == "switch":
        component = Switch.parse_csv(values)
    elif comp_type == "sensor":
        component = Sensor.parse_csv(values)
    elif comp_type == "led light":
        component = LEDLight.parse_csv(values)
    elif comp_type == "light globe":
        component = LightGlobe.parse_csv(values)
    elif comp_type == "buzzer":
        component = Buzzer.parse_csv(values)
    else:
        raise ValueError(f"Unknown component type: {values[0]}")

    return (quantity, component)


# ----------------------------------
# Circuit Kit Classes
# ----------------------------------

class CircuitKit(ABC):
    """
    Base class for Circuit Kits.
    - Has a name
    - Holds a list of (quantity, component) tuples
    - Price is sum of each component's price * quantity
    - Must implement add_component, remove_component, check completeness, etc.
    """

    def __init__(self, kit_name: str):
        self.kit_name = kit_name
        self.components = []  # list of (quantity, Component)

    def add_component(self, quantity: int, component: Component):
        self.components.append((quantity, component))

    def remove_component(self, component: Component):
        """
        Remove the *first occurrence* of the given component from the kit list,
        ignoring quantity for simplicity. (Could be extended to handle partial removal.)
        """
        for i, (qty, comp) in enumerate(self.components):
            if comp == component:
                self.components.pop(i)
                return

    def total_price(self) -> float:
        """Sum of (component.price * quantity)."""
        return sum(qty * comp.price for qty, comp in self.components)

    def total_components_count(self) -> int:
        """Sum of all quantities of components."""
        return sum(qty for qty, _ in self.components)

    def power_supplies(self):
        """
        Return a list of (quantity, component) for any power-supply type components
        (Battery or SolarPanel).
        """
        result = []
        for qty, comp in self.components:
            if isinstance(comp, Battery) or isinstance(comp, SolarPanel):
                result.append((qty, comp))
        return result

    @abstractmethod
    def is_complete(self) -> bool:
        """
        Checks if this circuit kit meets all the rules to be 'complete' and sellable.
        Must be overridden by subclasses (LightCircuitKit, SensorCircuitKit, etc.).
        """
        pass

    def __eq__(self, other):
        """
        Compare if two circuit kits are equal (by same type and same sorted sets of components).
        """
        if not isinstance(other, CircuitKit):
            return False
        if type(self) != type(other):
            return False
        if self.kit_name != other.kit_name:
            return False
        # Compare sorted lists of components (by display string for simplicity)
        self_comp_list = sorted(
            [f"{qty}x {comp.display_string()}" for qty, comp in self.components]
        )
        other_comp_list = sorted(
            [f"{qty}x {comp.display_string()}" for qty, comp in other.components]
        )
        return self_comp_list == other_comp_list

    def summary_display(self) -> str:
        """
        Example for a Light CircuitKit:
        "21 Piece Light Circuit, with 2 AA Batteries, 4 Warm Light Globes & Push Switch"
        (This will be overridden by each specialized kit to provide the exact summary.)
        """
        return f"{self.total_components_count()} Piece {self.kit_name}"

    def detail_display(self) -> str:
        """
        Show each component with quantity, e.g.:
        2 x 1.5V AA Battery $3.10
        4 x 6.5V 240.0mA Warm Light Globe $3.50
        ...
        (This can be overridden if you need more specialized formatting.)
        """
        lines = [f"{self.summary_display()}"]
        for qty, comp in self.components:
            lines.append(f"{qty} x {comp.display_string()}")
        return "\n".join(lines)


class LightCircuitKit(CircuitKit):
    """
    Subclass for "Light Circuit" rules:
      - Must have at least one battery (and no solar panels).
      - Must have at least one light.
      - All lights must be the same type (LED or Light Globe).
         * If LED, colours can differ.
         * If Light Globe, colours must be the same.
      - Must have at least the same number of wires as all other components combined.
      - Must have at least one switch (all switches same type).
      - No sensors allowed.
      - Display the number of unique colours, the number of switches, the switch type, etc.
    """

    def __init__(self):
        super().__init__("Light Circuit")

    def is_complete(self) -> bool:
        # Check for power supply: at least one battery, no solar
        batteries = [(q, c) for q, c in self.components if isinstance(c, Battery)]
        solars = [(q, c) for q, c in self.components if isinstance(c, SolarPanel)]
        if not batteries or solars:
            return False

        # Must have lights
        lights = [(q, c) for q, c in self.components if isinstance(c, Light)]
        if not lights:
            return False

        # All lights same type?
        first_light_class = type(lights[0][1])
        for _, l_comp in lights:
            if type(l_comp) != first_light_class:
                return False

        # If Light Globe, all must have the same colour
        if first_light_class == LightGlobe:
            first_colour = lights[0][1].colour
            for _, l_comp in lights:
                if l_comp.colour != first_colour:
                    return False
            # (If the same colour, also check that other values match if needed.)

        # Must have at least one switch. All switches same type?
        switches = [(q, c) for q, c in self.components if isinstance(c, Switch)]
        if not switches:
            return False
        first_switch_type = switches[0][1].switch_type
        for _, s_comp in switches:
            if s_comp.switch_type != first_switch_type:
                return False

        # No sensors
        sensors = [(q, c) for q, c in self.components if isinstance(c, Sensor)]
        if sensors:
            return False

        # Check wires count >= number of other components
        wire_count = sum(q for q, c in self.components if isinstance(c, Wire))
        other_count = sum(q for q, c in self.components if not isinstance(c, Wire))
        if wire_count < other_count:
            return False

        return True

    def summary_display(self) -> str:
        """
        Example:
        "21 Piece Light Circuit, with 2 AA Batteries, 4 Warm Light Globes & Push Switch"
        plus the number of unique colours, the number/type of switches, etc.
        """
        piece_count = self.total_components_count()
        # Gather battery info
        batteries = [(q, c) for q, c in self.components if isinstance(c, Battery)]
        # We assume all batteries are same type
        total_batt_qty = sum(q for q, _ in batteries)
        if batteries:
            first_battery = batteries[0][1]
            battery_desc = f"{total_batt_qty} {first_battery.size} {first_battery.name}s"
            battery_voltage = f"{first_battery.voltage:.1f}V"
        else:
            battery_desc = "No Battery"
            battery_voltage = ""

        # Gather lights
        lights = [(q, c) for q, c in self.components if isinstance(c, Light)]
        total_lights_qty = sum(q for q, _ in lights)
        if lights:
            first_light = lights[0][1]
            if isinstance(first_light, LEDLight):
                light_type = "LED Lights"
            else:
                light_type = "Light Globes"
            # Count unique colours
            unique_colours = set()
            for q, l_comp in lights:
                unique_colours.add(l_comp.colour)
            # E.g. "4 Warm Light Globes" or "8 LED Lights [4 Red/4 Green]"
            light_desc = f"{total_lights_qty} {first_light.colour.capitalize()} {light_type}"
            if isinstance(first_light, LEDLight) and len(unique_colours) > 1:
                # If multiple LED colours, you might do something fancier
                light_desc = (f"{total_lights_qty} Multi Coloured {light_type} "
                              f"[{self._colour_breakdown(lights)}]")
        else:
            light_desc = "0 Lights"

        # Gather switches
        switches = [(q, c) for q, c in self.components if isinstance(c, Switch)]
        total_switch_qty = sum(q for q, _ in switches)
        switch_desc = ""
        if switches:
            first_switch = switches[0][1]
            switch_desc = f"{first_switch.switch_type.capitalize()} Switch"

        summary = (f"{piece_count} Piece {self.kit_name}, with {battery_desc}, "
                   f"{light_desc}")
        if switch_desc:
            summary += f" & {switch_desc}"
        return summary

    def _colour_breakdown(self, lights_list):
        """
        For multiple LED colours, produce a breakdown like "4 Red/4 Green".
        """
        colour_map = {}
        for qty, comp in lights_list:
            colour_map[comp.colour] = colour_map.get(comp.colour, 0) + qty
        # Build a string "4 Red/4 Green"
        parts = [f"{count} {colour.capitalize()}" for colour, count in colour_map.items()]
        return "/".join(parts)


class SensorCircuitKit(CircuitKit):
    """
    Subclass for "Sensor Circuit" rules:
      - Has a power source (battery or solar)
      - Only one sensor
      - Either lights (all same LED) or a single buzzer (but not both)
      - If multiple lights, must all match
      - Must have more wires than all other components
      - Switches are optional
    """

    def __init__(self):
        super().__init__("Sensor Circuit")

    def is_complete(self) -> bool:
        # Must have exactly one type of power source
        batteries = [(q, c) for q, c in self.components if isinstance(c, Battery)]
        solars = [(q, c) for q, c in self.components if isinstance(c, SolarPanel)]
        if not batteries and not solars:
            return False
        if batteries and solars:
            return False  # can't have both

        # Must have exactly one sensor
        sensors = [(q, c) for q, c in self.components if isinstance(c, Sensor)]
        total_sensors = sum(q for q, _ in sensors)
        if total_sensors != 1:
            return False

        # Either buzzer or lights (not both)
        buzzers = [(q, c) for q, c in self.components if isinstance(c, Buzzer)]
        lights = [(q, c) for q, c in self.components if isinstance(c, Light)]
        if buzzers and lights:
            return False

        # If we have buzzers, only 1
        if buzzers:
            total_buzzers = sum(q for q, _ in buzzers)
            if total_buzzers != 1:
                return False

        # If we have lights, must be LED and must all match (same type, colour, voltage, current)
        if lights:
            # Must all be LEDLight, and must match exactly
            for _, lt in lights:
                if not isinstance(lt, LEDLight):
                    return False
            # Check that all LED lights have same attributes
            first_light = lights[0][1]
            for _, lt in lights:
                if not (lt.colour == first_light.colour and
                        abs(lt.voltage - first_light.voltage) < 1e-9 and
                        abs(lt.current - first_light.current) < 1e-9):
                    return False

        # Must have more wires than total of other components
        wire_count = sum(q for q, c in self.components if isinstance(c, Wire))
        others_count = sum(q for q, c in self.components if not isinstance(c, Wire))
        if wire_count <= others_count:
            return False

        return True

    def summary_display(self) -> str:
        """
        Example:
        "8 Piece Sensor Circuit, with Solar Panel, Motion Sensor, Buzzer & Toggle Switch"
        or
        "6 Piece Sensor Circuit, with AA Battery, Dust Sensor & Red LED Light"
        """
        piece_count = self.total_components_count()
        # Identify power supply
        batteries = [(q, c) for q, c in self.components if isinstance(c, Battery)]
        solars = [(q, c) for q, c in self.components if isinstance(c, SolarPanel)]
        power_desc = ""
        if batteries:
            # Assume they're all identical
            total_batt_qty = sum(q for q, _ in batteries)
            first_batt = batteries[0][1]
            power_desc = f"{total_batt_qty} {first_batt.size} {first_batt.name}"
        elif solars:
            # Assume they're all identical
            total_solar_qty = sum(q for q, _ in solars)
            first_solar = solars[0][1]
            power_desc = f"{total_solar_qty} {first_solar.name}"

        # Identify sensor
        sensors = [(q, c) for q, c in self.components if isinstance(c, Sensor)]
        sensor_desc = ""
        if sensors:
            # There's exactly one sensor
            s = sensors[0][1]
            sensor_desc = f"{s.sensor_type.capitalize()} {s.name}"

        # Buzzer or Lights
        buzzers = [(q, c) for q, c in self.components if isinstance(c, Buzzer)]
        lights = [(q, c) for q, c in self.components if isinstance(c, Light)]
        out_desc = ""
        if buzzers:
            out_desc = "Buzzer"
        elif lights:
            total_lights_qty = sum(q for q, _ in lights)
            first_light = lights[0][1]
            out_desc = f"{total_lights_qty} {first_light.colour.capitalize()} {first_light.name}"

        # Switches (could be zero or more)
        switches = [(q, c) for q, c in self.components if isinstance(c, Switch)]
        switch_desc = ""
        if switches:
            # E.g. "Toggle Switch"
            first_switch = switches[0][1]
            switch_desc = f"{first_switch.switch_type.capitalize()} Switch"

        # Build summary
        parts = [f"{piece_count} Piece {self.kit_name}, with {power_desc}, {sensor_desc}"]
        if out_desc:
            parts.append(out_desc)
        if switch_desc:
            parts.append(f"& {switch_desc}")
        summary = " ".join(parts)
        # Clean minor spacing issues
        summary = summary.replace(", &", ", &")  # example fix
        return summary


# ----------------------------------
# Example Usage / Testing
# ----------------------------------

if __name__ == "__main__":
    # Example: parse a single component from CSV
    csv_line = "17,Wire,40,2.4"
    parts = csv_line.split(",")  # ["17", "Wire", "40", "2.4"]
    quantity = int(parts[0])
    component_values = parts[1:]
    qty, wire_component = parse_single_component_from_csv(quantity, component_values)
    print(qty, wire_component.display_string())  # 17 40mm Wire $2.40

    # Build a LightCircuitKit from multiple components
    kit = LightCircuitKit()
    # Add 2 AA batteries
    b = Battery("AA", 1.5, 3.1)
    kit.add_component(2, b)
    # Add 4 Warm Light Globes
    lg = LightGlobe("warm", 6.5, 240, 3.5)
    kit.add_component(4, lg)
    # Add 14 wires
    w = Wire(60, 3.2)
    kit.add_component(14, w)
    # Add 1 push switch
    sw = Switch("push", 4.5, 4.6)
    kit.add_component(1, sw)

    print("\n--- LightCircuitKit Summary ---")
    print(kit.summary_display())
    print("\n--- LightCircuitKit Details ---")
    print(kit.detail_display())
    print(f"\nIs kit complete? {kit.is_complete()}")
    print(f"Total kit price: ${kit.total_price():.2f}")
