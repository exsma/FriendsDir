"""Factory robots for Ubermelon."""

import random

##############################################################################
# DON'T EDIT THIS FILE


class Robot(object):
    """Base class for all robots."""

    robot_name = 'Generic MelonBot'

    def display_status(self, msg):
        """Print a robot status message."""

        print("{} Status: {}".format(self.robot_name, msg))


class PickerBot(Robot):
    """Robots that handles picking of melons."""

    robot_name = 'PickerBot'

    def pick(self, melon):
        """Set characteristics of the melon that was picked."""

        weight = 10 * random.random()
        melon.weight = weight

        if melon.melon_type == 'Winter Squash':
            melon.color = 'Yellow'

        else:
            melon.color = 'Green'

        self.display_status("Picked a {}".format(melon))


class CleanerBot(Robot):
    """Robot that cleans melons."""

    robot_name = 'CleanerBot'

    def clean(self, melon):
        """Clean a melon."""

        self.display_status("Cleaned a {}".format(melon))


class StickerBot(Robot):
    """Robot that attached stickers."""

    robot_name = "StickerBot"

    def apply_logo(self, melon):
        """Apply logo stickers."""

        if random.random() < .9:
            melon.stickers.append('UberMelon Logo')
        if random.random() < .9:
            melon.stickers.append('Satisfaction Guaranteed')

        self.display_status("Applied logos to a {}".format(melon))


class InspectorBot(Robot):
    """Robot that inspects a melon for quality standards."""

    robot_name = 'InspectorBot 2000'

    def evaluate(self, melon):
        """Evaluate a melon for quality. Return True if ok, False if not."""
        self.display_status("Evaluating a {}".format(melon))

        # Melons less than 3LB don't meet our quality standards
        if melon.weight < 3:
            self.display_status("{} weight less than 3lbs!  REJECTED!!".format(melon))
            return False

        # Melons over 8LB cost too much to ship!
        if melon.weight > 8:
            self.display_status("{} weight over 8lbs!  REJECTED!!".format(melon))
            return False

        # Melons should have two stickers applied
        if len(melon.stickers) < 2:
            self.display_status("{} is not labeled correctly!  REJECTED!!".format(melon))
            return False

        # All melons should be green!
        if melon.color != 'Green':
            self.display_status("{} is not Green!  ".format(melon) +
                "All melons must be Green!  REJECTED!!")
            return False

        self.display_status("{} Passes".format(melon))

        return True


class PackerBot(Robot):
    """Robot that packs melons."""

    robot_name = 'PackerBot'

    def pack(self, melons):
        """Pack melons into boxes and return the list of boxes."""

        box = Box()
        boxes = [box]

        for melon in melons:
            self.display_status("Packing {}".format(melon))

            # If the current box is over the limit, get a new box
            if box.at_limit():
                box = Box()
                boxes.append(box)

            box.add_to_box(melon)

        return boxes


class ShipperBot(Robot):
    """Robot that ships melons."""

    robot_name = 'ShipperBot'

    def ship(self, boxes):
        """Ship boxes of melons."""

        self.display_status("Shipping {} boxes of melons.".format(len(boxes)))

        for i in range(len(boxes)):
            self.display_status(
                "Box {} Weight: {:.2f} lbs".format(i + 1, boxes[i].weight()))


class TrashBot(Robot):
    """Robot that handles disposing of bad melons."""

    robot_name = 'TrashBot'

    def trash(self, melon):
        """Take melon to the trash."""

        self.display_status("Sending {} to the compost".format(melon))


class PainterBot(Robot):
    """Robot that paints melons."""

    robot_name = 'PainterBot'

    def paint(self, melon):
        """Paint a melon green."""

        self.display_status("Painting {} Green".format(melon))
        melon.color = 'Green'


##############################################################################


class Box(object):
    """Box for packing melons in."""

    max_melons = 5

    def __init__(self):
        # Make a contents attribute for boxes. We do this here, rather than
        # as a class attribute, so that not all boxes share the same list--
        # otherwise, as you mutated "a box's contents", you'd really be
        # changing ALL boxes contents.

        self.contents = []

    def at_limit(self):
        """Is this box at limit?"""

        return len(self.contents) >= self.max_melons

    def add_to_box(self, melon):
        """Add melon to box; return True if successful."""

        if self.at_limit():
            print("Box is full! Dropped melon on the floor!")
            return False

        self.contents.append(melon)

        return True

    def weight(self):
        """Return weight of box."""

        return sum([item.weight for item in self.contents])

    def display_contents(self):
        """Display contents of box."""

        output = "|"
        for m in self.contents:
            output += " {} |".format(m)

        return output

    def __str__(self):
        """Return contents of box.

        __str__() is a method on classes that decides what gets printed
        if you just print an instance. By having a __str__ method, we will
        get customized output if we just print a box.
        """

        return "Box contains: {}".format(self.display_contents())


##############################################################################

# Instantiate some Robots

random.seed()

pickerbot    = PickerBot()
cleanerbot   = CleanerBot()
stickerbot   = StickerBot()
inspectorbot = InspectorBot()
trashbot     = TrashBot()
packerbot    = PackerBot()
shipperbot   = ShipperBot()
painterbot   = PainterBot()
