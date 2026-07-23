from typing import Dict, List, Optional, Tuple, Union
import cairo
import numpy as np
from bemve.vmobject import VMobject


# ============================================================================
# 1. ARRAYS & SORTING PRIMITIVES
# ============================================================================

class ArrayMobject(VMobject):
    """
    An interactive, animatable Array Mobject designed for sorting, searching,
    and two-pointer algorithm visualizers.
    """

    def __init__(
        self,
        values: List[Union[int, float, str]],
        box_size: float = 0.8,
        position: Tuple[float, float] = (0.0, 0.0),
        show_indices: bool = True,
        border_color: Tuple[float, float, float, float] = (0.0, 0.9, 1.0, 1.0),
        fill_color: Tuple[float, float, float, float] = (0.12, 0.14, 0.18, 0.95),
        text_color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
    ):
        super().__init__()
        self.values = values
        self.box_size = box_size
        self.position = np.array(position, dtype=float)
        self.show_indices = show_indices
        self.border_color = border_color
        self.fill_color = fill_color
        self.text_color = text_color

        # State highlights: {index: (r, g, b, a)}
        self.highlights: Dict[int, Tuple[float, float, float, float]] = {}
        # Pointer labels: {index: ("Pointer Name", color)}
        self.pointers: Dict[int, Tuple[str, Tuple[float, float, float, float]]] = {}

    def set_highlight(self, index: int, color: Tuple[float, float, float, float]):
        """Highlights a cell at a given index with a specific RGBA color."""
        if 0 <= index < len(self.values):
            self.highlights[index] = color

    def set_range_highlight(
        self, start: int, end: int, color: Tuple[float, float, float, float]
    ):
        """Highlights a contiguous slice of the array."""
        for i in range(max(0, start), min(len(self.values), end + 1)):
            self.highlights[i] = color

    def clear_highlights(self):
        """Removes all active cell highlights."""
        self.highlights.clear()

    def set_pointer(
        self,
        index: int,
        label: str,
        color: Tuple[float, float, float, float] = (1.0, 0.3, 0.3, 1.0),
    ):
        """Attaches a named pointer arrow above or below an array cell."""
        if 0 <= index < len(self.values):
            self.pointers[index] = (label, color)

    def clear_pointers(self):
        """Clears all attached pointers."""
        self.pointers.clear()

    def swap(self, i: int, j: int):
        """Swaps two values inside the array state."""
        if 0 <= i < len(self.values) and 0 <= j < len(self.values):
            self.values[i], self.values[j] = self.values[j], self.values[i]

    def draw(self, ctx: cairo.Context):
        ctx.save()
        total_width = len(self.values) * self.box_size
        start_x = self.position[0] - (total_width / 2.0)
        start_y = self.position[1]

        for i, val in enumerate(self.values):
            x = start_x + (i * self.box_size)
            y = start_y

            # 1. Fill Box
            ctx.rectangle(x, y, self.box_size, self.box_size)
            if i in self.highlights:
                ctx.set_source_rgba(*self.highlights[i])
            else:
                ctx.set_source_rgba(*self.fill_color)
            ctx.fill_preserve()

            # 2. Draw Border
            ctx.set_source_rgba(*self.border_color)
            ctx.set_line_width(0.03)
            ctx.stroke()

            # 3. Value Text
            ctx.save()
            ctx.set_source_rgba(*self.text_color)
            ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(self.box_size * 0.4)
            extents = ctx.text_extents(str(val))
            text_x = x + (self.box_size / 2.0) - (extents.width / 2.0 + extents.x_bearing)
            text_y = y + (self.box_size / 2.0) - (extents.height / 2.0 + extents.y_bearing)
            ctx.move_to(text_x, text_y)
            ctx.show_text(str(val))
            ctx.restore()

            # 4. Optional Index Numbering Below Cell
            if self.show_indices:
                ctx.save()
                ctx.set_source_rgba(0.6, 0.6, 0.7, 0.9)
                ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                ctx.set_font_size(self.box_size * 0.25)
                idx_str = f"[{i}]"
                idx_ext = ctx.text_extents(idx_str)
                idx_x = x + (self.box_size / 2.0) - (idx_ext.width / 2.0 + idx_ext.x_bearing)
                idx_y = y + self.box_size + (self.box_size * 0.35)
                ctx.move_to(idx_x, idx_y)
                ctx.show_text(idx_str)
                ctx.restore()

            # 5. Pointer Arrow & Label Above Cell
            if i in self.pointers:
                ptr_label, ptr_color = self.pointers[i]
                ctx.save()
                ptr_x = x + (self.box_size / 2.0)
                ptr_y = y - 0.15
                
                # Draw Arrow Head
                ctx.set_source_rgba(*ptr_color)
                ctx.move_to(ptr_x, ptr_y)
                ctx.line_to(ptr_x - 0.1, ptr_y - 0.2)
                ctx.line_to(ptr_x + 0.1, ptr_y - 0.2)
                ctx.close_path()
                ctx.fill()

                # Draw Pointer Label
                ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                ctx.set_font_size(0.22)
                lbl_ext = ctx.text_extents(ptr_label)
                ctx.move_to(
                    ptr_x - (lbl_ext.width / 2.0 + lbl_ext.x_bearing),
                    ptr_y - 0.28 - (lbl_ext.height + lbl_ext.y_bearing),
                )
                ctx.show_text(ptr_label)
                ctx.restore()

        ctx.restore()


# ============================================================================
# 2. LINKED LIST & POINTER GRAPH NODES
# ============================================================================

class LinkedListNode(VMobject):
    """
    A multi-compartment Linked List Node showing Data and Next/Prev Pointer fields.
    """

    def __init__(
        self,
        value: str,
        position: Tuple[float, float] = (0.0, 0.0),
        width: float = 1.2,
        height: float = 0.7,
        node_color: Tuple[float, float, float, float] = (0.2, 0.6, 1.0, 1.0),
    ):
        super().__init__()
        self.value = str(value)
        self.position = np.array(position, dtype=float)
        self.width = width
        self.height = height
        self.node_color = node_color
        self.highlight_color: Optional[Tuple[float, float, float, float]] = None

    def draw(self, ctx: cairo.Context):
        ctx.save()
        x, y = self.position[0] - (self.width / 2.0), self.position[1] - (self.height / 2.0)

        # Draw Node Body
        ctx.rectangle(x, y, self.width, self.height)
        if self.highlight_color:
            ctx.set_source_rgba(*self.highlight_color)
        else:
            ctx.set_source_rgba(0.1, 0.12, 0.16, 0.9)
        ctx.fill_preserve()

        ctx.set_source_rgba(*self.node_color)
        ctx.set_line_width(0.03)
        ctx.stroke()

        # Split Divider (Data | Next)
        ctx.move_to(x + (self.width * 0.65), y)
        ctx.line_to(x + (self.width * 0.65), y + self.height)
        ctx.stroke()

        # Data Text
        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(self.height * 0.4)
        extents = ctx.text_extents(self.value)
        ctx.move_to(
            x + (self.width * 0.325) - (extents.width / 2.0 + extents.x_bearing),
            y + (self.height / 2.0) - (extents.height / 2.0 + extents.y_bearing),
        )
        ctx.show_text(self.value)

        # Pointer Dot inside Next field
        ctx.arc(x + (self.width * 0.825), y + (self.height / 2.0), 0.05, 0, 2 * np.pi)
        ctx.fill()

        ctx.restore()


class PointerArrow:
    """Utility class for drawing smooth directional connections between nodes."""

    @staticmethod
    def draw(
        ctx: cairo.Context,
        start_pos: Tuple[float, float],
        end_pos: Tuple[float, float],
        color: Tuple[float, float, float, float] = (1.0, 0.3, 0.5, 1.0),
        label: Optional[str] = None,
        curved: bool = False,
    ):
        ctx.save()
        ctx.set_source_rgba(*color)
        ctx.set_line_width(0.035)

        x1, y1 = start_pos
        x2, y2 = end_pos

        if not curved:
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()
            angle = np.arctan2(y2 - y1, x2 - x1)
        else:
            # Quadratic Bezier curve for recursive/cycle pointers
            ctrl_x = (x1 + x2) / 2.0 + (y1 - y2) * 0.4
            ctrl_y = (y1 + y2) / 2.0 + (x2 - x1) * 0.4
            ctx.move_to(x1, y1)
            ctx.quadratic_curve_to(ctrl_x, ctrl_y, x2, y2)
            ctx.stroke()
            angle = np.arctan2(y2 - ctrl_y, x2 - ctrl_x)

        # Arrowhead
        arrow_size = 0.12
        ctx.move_to(x2, y2)
        ctx.line_to(
            x2 - arrow_size * np.cos(angle - np.pi / 6),
            y2 - arrow_size * np.sin(angle - np.pi / 6),
        )
        ctx.line_to(
            x2 - arrow_size * np.cos(angle + np.pi / 6),
            y2 - arrow_size * np.sin(angle + np.pi / 6),
        )
        ctx.close_path()
        ctx.fill()

        # Optional Edge Weight/Label
        if label:
            mid_x = (x1 + x2) / 2.0
            mid_y = (y1 + y2) / 2.0 - 0.12
            ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(0.2)
            ctx.move_to(mid_x, mid_y)
            ctx.show_text(label)

        ctx.restore()


# ============================================================================
# 3. BINARY TREES & GRAPH VISUALIZERS
# ============================================================================

class TreeNode:
    """Helper structure for recursively defining Binary Trees."""

    def __init__(self, value: Union[int, str], left=None, right=None):
        self.value = str(value)
        self.left: Optional[TreeNode] = left
        self.right: Optional[TreeNode] = right
        self.position: np.ndarray = np.array([0.0, 0.0])
        self.highlight_color: Optional[Tuple[float, float, float, float]] = None


class BinaryTreeMobject(VMobject):
    """
    Auto-positioning Binary Tree / Heap renderer with node highlighting
    and traversal animation state tracking.
    """

    def __init__(
        self,
        root: TreeNode,
        radius: float = 0.35,
        vertical_spacing: float = 1.0,
        horizontal_spacing: float = 3.5,
        center_pos: Tuple[float, float] = (0.0, 2.0),
    ):
        super().__init__()
        self.root = root
        self.radius = radius
        self.vertical_spacing = vertical_spacing
        self.horizontal_spacing = horizontal_spacing
        self.center_pos = np.array(center_pos, dtype=float)
        
        # Calculate auto layout coordinates
        self._calculate_positions(self.root, self.center_pos[0], self.center_pos[1], level=1)

    def _calculate_positions(self, node: Optional[TreeNode], x: float, y: float, level: int):
        if not node:
            return
        node.position = np.array([x, y], dtype=float)
        offset = self.horizontal_spacing / (2 ** level)
        
        if node.left:
            self._calculate_positions(node.left, x - offset, y - self.vertical_spacing, level + 1)
        if node.right:
            self._calculate_positions(node.right, x + offset, y - self.vertical_spacing, level + 1)

    def draw(self, ctx: cairo.Context):
        self._draw_edges(ctx, self.root)
        self._draw_nodes(ctx, self.root)

    def _draw_edges(self, ctx: cairo.Context, node: Optional[TreeNode]):
        if not node:
            return
        for child in [node.left, node.right]:
            if child:
                ctx.save()
                ctx.set_source_rgba(0.4, 0.5, 0.7, 0.8)
                ctx.set_line_width(0.03)
                ctx.move_to(node.position[0], node.position[1])
                ctx.line_to(child.position[0], child.position[1])
                ctx.stroke()
                ctx.restore()
                self._draw_edges(ctx, child)

    def _draw_nodes(self, ctx: cairo.Context, node: Optional[TreeNode]):
        if not node:
            return
        ctx.save()
        x, y = node.position

        # Circle Fill
        ctx.arc(x, y, self.radius, 0, 2 * np.pi)
        if node.highlight_color:
            ctx.set_source_rgba(*node.highlight_color)
        else:
            ctx.set_source_rgba(0.12, 0.15, 0.22, 0.95)
        ctx.fill_preserve()

        # Stroke Border
        ctx.set_source_rgba(0.0, 0.8, 1.0, 1.0)
        ctx.set_line_width(0.035)
        ctx.stroke()

        # Label Text
        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(self.radius * 0.75)
        extents = ctx.text_extents(node.value)
        ctx.move_to(
            x - (extents.width / 2.0 + extents.x_bearing),
            y - (extents.height / 2.0 + extents.y_bearing),
        )
        ctx.show_text(node.value)
        ctx.restore()

        self._draw_nodes(ctx, node.left)
        self._draw_nodes(ctx, node.right)


# ============================================================================
# 4. CODE BLOCK SYNTAX TRACKER
# ============================================================================

class CodeBlockMobject(VMobject):
    """
    Displays pseudocode or source code with live line-number highlighting,
    ideal for stepping through algorithm loops and recursive calls.
    """

    def __init__(
        self,
        code_lines: List[str],
        position: Tuple[float, float] = (-3.0, 1.5),
        font_size: float = 0.25,
        title: str = "Algorithm Execution",
    ):
        super().__init__()
        self.code_lines = code_lines
        self.position = np.array(position, dtype=float)
        self.font_size = font_size
        self.title = title
        self.active_line: Optional[int] = None

    def set_active_line(self, line_num: int):
        """Highlights a specific active line of code (1-indexed)."""
        self.active_line = line_num

    def clear_active_line(self):
        """Removes code line highlighting."""
        self.active_line = None

    def draw(self, ctx: cairo.Context):
        ctx.save()
        start_x, start_y = self.position
        line_height = self.font_size * 1.6
        max_width = max(len(line) for line in self.code_lines) * (self.font_size * 0.6) + 0.8
        total_height = (len(self.code_lines) + 1) * line_height + 0.3

        # Background Container Window
        ctx.rectangle(start_x, start_y - 0.4, max_width, total_height)
        ctx.set_source_rgba(0.08, 0.09, 0.12, 0.95)
        ctx.fill_preserve()
        ctx.set_source_rgba(0.2, 0.25, 0.35, 1.0)
        ctx.set_line_width(0.02)
        ctx.stroke()

        # Window Title Bar
        ctx.rectangle(start_x, start_y - 0.4, max_width, 0.35)
        ctx.set_source_rgba(0.15, 0.18, 0.25, 1.0)
        ctx.fill()
        
        ctx.set_source_rgba(0.7, 0.8, 0.9, 1.0)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(0.18)
        ctx.move_to(start_x + 0.2, start_y - 0.18)
        ctx.show_text(f"❖ {self.title}")

        # Render Lines
        ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(self.font_size)

        for idx, line in enumerate(self.code_lines):
            line_num = idx + 1
            curr_y = start_y + (idx + 1) * line_height

            # Highlight Active Executing Line
            if self.active_line == line_num:
                ctx.rectangle(start_x + 0.05, curr_y - (self.font_size * 0.9), max_width - 0.1, line_height)
                ctx.set_source_rgba(0.9, 0.6, 0.1, 0.35)
                ctx.fill()

                # Highlight Marker
                ctx.set_source_rgba(1.0, 0.7, 0.0, 1.0)
                ctx.move_to(start_x + 0.1, curr_y - 0.05)
                ctx.show_text("▶")

            # Line Numbers
            ctx.set_source_rgba(0.4, 0.45, 0.55, 1.0)
            ctx.move_to(start_x + 0.3, curr_y)
            ctx.show_text(f"{line_num:2d} ")

            # Code Content
            ctx.set_source_rgba(0.9, 0.95, 1.0, 1.0)
            ctx.move_to(start_x + 0.7, curr_y)
            ctx.show_text(line)

        ctx.restore()


# ============================================================================
# 5. STACKS & QUEUES
# ============================================================================

class StackMobject(VMobject):
    """Animatable LIFO Stack structure showing Push and Pop operations."""

    def __init__(
        self,
        capacity: int = 5,
        width: float = 1.2,
        height: float = 2.5,
        position: Tuple[float, float] = (3.0, 0.0),
    ):
        super().__init__()
        self.capacity = capacity
        self.width = width
        self.height = height
        self.position = np.array(position, dtype=float)
        self.items: List[str] = []

    def push(self, val: str):
        if len(self.items) < self.capacity:
            self.items.append(str(val))

    def pop(self) -> Optional[str]:
        return self.items.pop() if self.items else None

    def draw(self, ctx: cairo.Context):
        ctx.save()
        x, y = self.position[0] - (self.width / 2.0), self.position[1] - (self.height / 2.0)

        # U-shaped Stack Bucket
        ctx.move_to(x, y)
        ctx.line_to(x, y + self.height)
        ctx.line_to(x + self.width, y + self.height)
        ctx.line_to(x + self.width, y)
        ctx.set_source_rgba(0.0, 0.8, 1.0, 1.0)
        ctx.set_line_width(0.04)
        ctx.stroke()

        # Render Stack Items from bottom up
        slot_height = self.height / self.capacity
        for i, item in enumerate(self.items):
            item_y = y + self.height - ((i + 1) * slot_height)
            
            ctx.rectangle(x + 0.05, item_y + 0.02, self.width - 0.1, slot_height - 0.04)
            ctx.set_source_rgba(0.2, 0.7, 0.4, 0.9)
            ctx.fill_preserve()
            ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            ctx.set_line_width(0.02)
            ctx.stroke()

            # Item Text Label
            ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(slot_height * 0.4)
            ext = ctx.text_extents(item)
            ctx.move_to(
                x + (self.width / 2.0) - (ext.width / 2.0 + ext.x_bearing),
                item_y + (slot_height / 2.0) - (ext.height / 2.0 + ext.y_bearing),
            )
            ctx.show_text(item)

        ctx.restore()
