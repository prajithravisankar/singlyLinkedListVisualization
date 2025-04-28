# --- START OF FILE ui/gui.py ---

import pygame
import sys
import json
import math # For gradient calculations if needed, or other math functions
from pygame.locals import *
from core.linked_list import LinkedList
from core.node import Node # Although LinkedList handles Node creation, importing helps with type hinting if needed

class TriviaGameGUI:
    """
    Manages the Pygame GUI for the Trivia Trek game. (Visually Enhanced Version)
    Visualizes the linked list, handles user interaction via buttons,
    and displays game state with improved aesthetics.
    """
    def __init__(self, screen_width=1000, screen_height=650): # Increased height slightly
        # --- Pygame Setup ---
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Trivia Trek: Linked List Challenge ✨')
        self.clock = pygame.time.Clock()

        # --- Enhanced Colors ---
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.LIGHT_GRAY = (230, 230, 230)
        self.DARK_GRAY = (100, 100, 100)
        self.GREEN = (60, 179, 113) # Medium Sea Green
        self.RED = (220, 20, 60)    # Crimson
        self.BLUE = (70, 130, 180)  # Steel Blue (Node)
        self.NODE_SHADOW = (50, 90, 130) # Darker blue for shadow
        self.YELLOW = (255, 193, 7)    # Amber (Highlight)
        self.DARK_RED = (139, 0, 0)     # Dark Red
        self.DARK_GREEN = (0, 100, 0)   # Dark Green
        self.BG_GRADIENT_TOP = (210, 220, 240) # Light blue/gray
        self.BG_GRADIENT_BOTTOM = (170, 180, 200) # Slightly darker

        # --- Fonts ---
        try:
            self.FONT_SMALL = pygame.font.SysFont('Arial', 14)
            self.FONT_MEDIUM = pygame.font.SysFont('Arial', 18)
            self.FONT_LARGE = pygame.font.SysFont('Arial', 24)
            self.FONT_XLARGE = pygame.font.SysFont('Arial', 48)
            self.FONT_ICON = pygame.font.SysFont('Arial', 20) # For feedback icons
        except pygame.error:
            print("Warning: Arial font not found, using default.")
            self.FONT_SMALL = pygame.font.Font(None, 20)
            self.FONT_MEDIUM = pygame.font.Font(None, 26)
            self.FONT_LARGE = pygame.font.Font(None, 32)
            self.FONT_XLARGE = pygame.font.Font(None, 56)
            self.FONT_ICON = pygame.font.Font(None, 28)


        # --- Layout & Game Elements ---
        self.HEADER_HEIGHT = 100
        self.FOOTER_HEIGHT = 120 # Keep footer height
        self.NODE_AREA_Y = self.HEADER_HEIGHT
        self.NODE_AREA_HEIGHT = self.screen_height - self.HEADER_HEIGHT - self.FOOTER_HEIGHT

        self.NODE_WIDTH = 240
        self.NODE_HEIGHT = 140
        self.NODE_PADDING = 10
        self.NODE_SHADOW_OFFSET = 4
        self.ARROW_LENGTH = 70
        self.BUTTON_WIDTH = 160
        self.BUTTON_HEIGHT = 50
        self.BUTTON_ROUNDING = 12
        self.SCROLL_SPEED = 30
        self.NODE_Y_POSITION = self.NODE_AREA_Y + (self.NODE_AREA_HEIGHT - self.NODE_HEIGHT) // 2 # Center vertically

        # --- Game State ---
        self.linked_list = LinkedList()
        self.score = 0
        self.game_over = False
        self.scroll_offset = 0
        self.feedback_message = ""
        self.feedback_icon = ""
        self.feedback_color = self.BLACK
        self.feedback_timer = 0
        self.total_nodes = 0

        # --- Load Data & Setup ---
        self.load_questions()
        self.create_buttons()

    def load_questions(self):
        """Loads trivia questions from questions.json into the linked list."""
        try:
            # Adjust path if running from main.py in root. If running gui.py directly, might need "data/questions.json"
            file_path = "data/questions.json"
            # Let's try relative to gui.py first for direct execution case, then fallback
            try:
                with open("../data/questions.json") as file:
                     dictionary = json.load(file)
            except FileNotFoundError:
                 # print("Trying path relative to project root...")
                 with open("data/questions.json") as file:
                      dictionary = json.load(file)

            if not dictionary:
                 raise ValueError("JSON file is empty.")
            for trivia in dictionary:
                if not all(k in trivia for k in ('question', 'answer', 'isCorrect')):
                     print(f"Warning: Skipping invalid trivia item: {trivia}")
                     continue
                self.linked_list.add_question(trivia['question'], trivia['answer'], trivia['isCorrect'])
            self.linked_list.current = self.linked_list.head
            temp = self.linked_list.head
            count = 0
            while temp:
                count += 1
                temp = temp.next
            self.total_nodes = count

        except FileNotFoundError:
            print(f"Error: data/questions.json not found. Searched relative to gui.py and project root.")
            self.feedback_message = "Error: questions.json not found!"
            self.feedback_icon = "❌"
            self.feedback_color = self.RED
            self.feedback_timer = 300
            self.linked_list.head = None
            self.linked_list.current = None
            self.total_nodes = 0
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error: Could not load or parse question data. Check format/content. Error: {e}")
            self.feedback_message = "Error: Invalid question data!"
            self.feedback_icon = "❌"
            self.feedback_color = self.RED
            self.feedback_timer = 300
            self.linked_list.head = None
            self.linked_list.current = None
            self.total_nodes = 0


    def create_buttons(self):
        """Creates the Rect objects for the UI buttons in the footer."""
        # Position buttons lower down in the footer area
        self.button_y = self.screen_height - self.BUTTON_HEIGHT - 20 # Y pos from bottom edge
        button_spacing = 30
        total_button_width = 3 * self.BUTTON_WIDTH + 2 * button_spacing
        start_x = (self.screen_width - total_button_width) // 2

        self.delete_button = pygame.Rect(start_x, self.button_y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.next_button = pygame.Rect(start_x + self.BUTTON_WIDTH + button_spacing, self.button_y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.confirm_button = pygame.Rect(start_x + 2 * (self.BUTTON_WIDTH + button_spacing), self.button_y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def draw_gradient_background(self):
        """Draws a vertical gradient background."""
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            color = (
                int(self.BG_GRADIENT_TOP[0] * (1 - ratio) + self.BG_GRADIENT_BOTTOM[0] * ratio),
                int(self.BG_GRADIENT_TOP[1] * (1 - ratio) + self.BG_GRADIENT_BOTTOM[1] * ratio),
                int(self.BG_GRADIENT_TOP[2] * (1 - ratio) + self.BG_GRADIENT_BOTTOM[2] * ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (self.screen_width, y))

    def draw_text(self, text, font, color, surface, x, y, center=False, center_x=False, center_y=False, max_width=None):
        """Enhanced helper function to draw text with better centering and wrapping."""
        if max_width:
            words = text.split(' ')
            lines = []
            current_line = ""
            line_surfaces = []
            total_height = 0
            line_height = font.get_linesize()

            for word in words:
                test_line = current_line + word + " "
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            lines.append(current_line.strip()) # Add the last line

            for line in lines:
                 line_surf = font.render(line, True, color)
                 line_surfaces.append(line_surf)
                 total_height += line_height

            start_y = y
            if center_y or center:
                start_y = y - total_height // 2

            current_y = start_y
            for i, line_surf in enumerate(line_surfaces):
                line_rect = line_surf.get_rect()
                line_x = x
                if center_x or center:
                    line_x = x # Use the provided x as the center for the rect
                    line_rect.centerx = line_x
                else:
                    line_rect.left = line_x # Align left if not centering x

                line_rect.top = current_y # Position based on previous line's bottom
                surface.blit(line_surf, line_rect)
                current_y += line_height


        else: # No wrapping needed
             text_surface = font.render(text, True, color)
             text_rect = text_surface.get_rect()
             if center:
                 text_rect.center = (x, y)
             elif center_x:
                  text_rect.centerx = x
                  text_rect.top = y
             elif center_y:
                  text_rect.centery = y
                  text_rect.left = x
             else:
                 text_rect.topleft = (x, y)
             surface.blit(text_surface, text_rect)


    def draw_node(self, node, x, y):
        """Draws a single node rectangle with improved styling."""
        adjusted_x = x - self.scroll_offset

        # Only draw if node is at least partially visible
        if adjusted_x + self.NODE_WIDTH > -50 and adjusted_x < self.screen_width + 50: # Slight buffer
            # --- Shadow ---
            shadow_rect = pygame.Rect(adjusted_x + self.NODE_SHADOW_OFFSET,
                                      y + self.NODE_SHADOW_OFFSET,
                                      self.NODE_WIDTH, self.NODE_HEIGHT)
            pygame.draw.rect(self.screen, self.NODE_SHADOW, shadow_rect, border_radius=self.BUTTON_ROUNDING)

            # --- Main Node Rect ---
            node_rect = pygame.Rect(adjusted_x, y, self.NODE_WIDTH, self.NODE_HEIGHT)
            pygame.draw.rect(self.screen, self.BLUE, node_rect, border_radius=self.BUTTON_ROUNDING)

            # --- Highlight Border ---
            if node == self.linked_list.current:
                pygame.draw.rect(self.screen, self.YELLOW, node_rect, 4, border_radius=self.BUTTON_ROUNDING)
            else:
                pygame.draw.rect(self.screen, self.NODE_SHADOW, node_rect, 1, border_radius=self.BUTTON_ROUNDING) # Subtle border


            # --- Content ---
            content_x = adjusted_x + self.NODE_PADDING
            content_y = y + self.NODE_PADDING
            content_width = self.NODE_WIDTH - 2 * self.NODE_PADDING
            available_height = self.NODE_HEIGHT - 2 * self.NODE_PADDING

            # Draw Question (wrapped)
            q_text = f"Q: {node.question}"
            q_font_height = self.FONT_SMALL.get_linesize()
            max_q_lines = (available_height // 2) // q_font_height # Approx max lines for question

            # Use draw_text's wrapping - estimate height based on result
            self.draw_text(q_text, self.FONT_SMALL, self.WHITE, self.screen,
                           content_x, content_y, max_width=content_width)
            # Need a better way to get actual height used by wrapped text
            # For now, estimate separator position based on available space
            separator_y = content_y + (available_height * 0.5) # Place separator halfway down content area

            # Draw Separator Line
            pygame.draw.line(self.screen, self.LIGHT_GRAY,
                             (content_x, separator_y),
                             (adjusted_x + self.NODE_WIDTH - self.NODE_PADDING, separator_y), 1)

            # Draw Answer (wrapped) - position below separator
            a_text = f"A: {node.answer}"
            answer_y = separator_y + 8 # Padding below separator
            self.draw_text(a_text, self.FONT_SMALL, self.WHITE, self.screen,
                           content_x, answer_y, max_width=content_width)


        return adjusted_x # Return adjusted x for arrow drawing


    def draw_arrow(self, start_x, start_y, end_x, end_y):
        """Draws a thicker arrow connecting two nodes."""
        mid_y = start_y + self.NODE_HEIGHT // 2
        arrow_start = (start_x + self.NODE_WIDTH, mid_y)
        arrow_end = (end_x, mid_y)

        # Only draw if arrow is potentially visible
        visible_start = start_x > -self.ARROW_LENGTH and start_x < self.screen_width
        visible_end = end_x > 0 and end_x < self.screen_width + self.ARROW_LENGTH
        spans_screen = start_x < 0 and end_x > self.screen_width

        if visible_start or visible_end or spans_screen:
            pygame.draw.line(self.screen, self.DARK_GRAY, arrow_start, arrow_end, 4) # Thicker line
            # Draw arrowhead
            try:
                # Prevent drawing polygon if start/end are too close (can cause ValueError)
                if abs(arrow_end[0] - arrow_start[0]) > 15:
                     pygame.draw.polygon(self.screen, self.DARK_GRAY, [
                         arrow_end,
                         (arrow_end[0] - 15, arrow_end[1] - 8), # Larger arrowhead
                         (arrow_end[0] - 15, arrow_end[1] + 8)
                     ])
            except ValueError:
                 pass


    def draw_list(self):
        """Draws the entire linked list with nodes and arrows."""
        current = self.linked_list.head
        x = 100 # Initial horizontal position off-screen left
        while current:
            adjusted_x = self.draw_node(current, x, self.NODE_Y_POSITION)
            if current.next:
                next_node_x = x + self.NODE_WIDTH + self.ARROW_LENGTH
                # Pass the adjusted x of the *next* node's potential start
                self.draw_arrow(adjusted_x, self.NODE_Y_POSITION, next_node_x - self.scroll_offset, self.NODE_Y_POSITION)
            x += self.NODE_WIDTH + self.ARROW_LENGTH
            current = current.next


    def draw_buttons(self):
        """Draws the action buttons with improved styling."""
        # Delete Button (Red)
        pygame.draw.rect(self.screen, self.RED, self.delete_button, border_radius=self.BUTTON_ROUNDING)
        pygame.draw.rect(self.screen, self.DARK_RED, self.delete_button, 3, border_radius=self.BUTTON_ROUNDING)
        self.draw_text("Delete (Wrong)", self.FONT_MEDIUM, self.WHITE, self.screen, self.delete_button.centerx, self.delete_button.centery, center=True)

        # Next Button (Gray)
        pygame.draw.rect(self.screen, self.GRAY, self.next_button, border_radius=self.BUTTON_ROUNDING)
        pygame.draw.rect(self.screen, self.DARK_GRAY, self.next_button, 3, border_radius=self.BUTTON_ROUNDING)
        self.draw_text("Next (Skip)", self.FONT_MEDIUM, self.BLACK, self.screen, self.next_button.centerx, self.next_button.centery, center=True)

        # Confirm Button (Green)
        pygame.draw.rect(self.screen, self.GREEN, self.confirm_button, border_radius=self.BUTTON_ROUNDING)
        pygame.draw.rect(self.screen, self.DARK_GREEN, self.confirm_button, 3, border_radius=self.BUTTON_ROUNDING)
        self.draw_text("Confirm (Correct)", self.FONT_MEDIUM, self.WHITE, self.screen, self.confirm_button.centerx, self.confirm_button.centery, center=True)

    def draw_header_footer(self):
         """Draws the header and footer areas."""
         header_rect = pygame.Rect(0, 0, self.screen_width, self.HEADER_HEIGHT)
         footer_rect = pygame.Rect(0, self.screen_height - self.FOOTER_HEIGHT, self.screen_width, self.FOOTER_HEIGHT)
         overlay_color = (*self.WHITE, 180)
         header_surf = pygame.Surface(header_rect.size, pygame.SRCALPHA)
         footer_surf = pygame.Surface(footer_rect.size, pygame.SRCALPHA)
         header_surf.fill(overlay_color)
         footer_surf.fill(overlay_color)
         self.screen.blit(header_surf, header_rect.topleft)
         self.screen.blit(footer_surf, footer_rect.topleft)

         # Title
         self.draw_text("Trivia Trek Challenge", self.FONT_LARGE, self.DARK_GRAY, self.screen, self.screen_width // 2, 30, center_x=True)
         # Score
         self.draw_text(f"Score: {self.score}", self.FONT_LARGE, self.BLUE, self.screen, self.screen_width - 100, 30, center=True)


         # --- FEEDBACK POSITION ADJUSTMENT ---
         # Calculate Y position relative to the *top* of the footer, well above the buttons
         feedback_area_top = self.screen_height - self.FOOTER_HEIGHT
         # Place it roughly in the middle of the space *above* the buttons
         feedback_y = feedback_area_top + (self.button_y - feedback_area_top) // 2 - 10 # Move up slightly more

         if self.feedback_timer > 0:
             icon_surf = self.FONT_ICON.render(self.feedback_icon, True, self.feedback_color)
             icon_rect = icon_surf.get_rect(centerx=self.screen_width // 2, centery=feedback_y - 10) # Icon above text

             # Draw text centered below the icon
             self.draw_text(self.feedback_message, self.FONT_MEDIUM, self.feedback_color, self.screen,
                            self.screen_width // 2, feedback_y + 10, center_x=True)

             self.screen.blit(icon_surf, icon_rect)
             self.feedback_timer -= 1
         else:
             self.feedback_message = ""
             self.feedback_icon = ""

    def draw_scroll_indicators(self):
        """Draws fixed scroll indicators at the screen edges."""
        indicator_y = self.NODE_Y_POSITION + self.NODE_HEIGHT // 2
        indicator_padding = 20
        indicator_bg_size = 40

        list_width = self.total_nodes * (self.NODE_WIDTH + self.ARROW_LENGTH) - self.ARROW_LENGTH if self.total_nodes > 0 else 0
        max_scroll = max(0, list_width - self.screen_width + 100) # Match scroll_view calc

        # Left Indicator
        if self.scroll_offset > 0:
            left_bg_rect = pygame.Rect(indicator_padding, indicator_y - indicator_bg_size // 2, indicator_bg_size, indicator_bg_size)
            pygame.draw.rect(self.screen, self.LIGHT_GRAY, left_bg_rect, border_radius=indicator_bg_size//2)
            pygame.draw.rect(self.screen, self.DARK_GRAY, left_bg_rect, 2, border_radius=indicator_bg_size//2)
            self.draw_text("◄", self.FONT_LARGE, self.BLACK, self.screen, left_bg_rect.centerx, left_bg_rect.centery, center=True)

        # Right Indicator
        if self.scroll_offset < max_scroll and self.total_nodes > 0:
            right_bg_rect = pygame.Rect(self.screen_width - indicator_padding - indicator_bg_size, indicator_y - indicator_bg_size // 2, indicator_bg_size, indicator_bg_size)
            pygame.draw.rect(self.screen, self.LIGHT_GRAY, right_bg_rect, border_radius=indicator_bg_size//2)
            pygame.draw.rect(self.screen, self.DARK_GRAY, right_bg_rect, 2, border_radius=indicator_bg_size//2)
            self.draw_text("►", self.FONT_LARGE, self.BLACK, self.screen, right_bg_rect.centerx, right_bg_rect.centery, center=True)


    def draw_game_over(self):
        """Draws the game over screen with better styling."""
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((*self.DARK_GRAY, 200))
        self.screen.blit(overlay, (0, 0))

        self.draw_text("Game Over!", self.FONT_XLARGE, self.YELLOW, self.screen, self.screen_width // 2, self.screen_height // 2 - 60, center=True)
        self.draw_text(f"Final Score: {self.score}", self.FONT_LARGE, self.WHITE, self.screen, self.screen_width // 2, self.screen_height // 2 + 10, center=True)
        self.draw_text("Press 'R' to Restart or 'Q' to Quit", self.FONT_MEDIUM, self.LIGHT_GRAY, self.screen, self.screen_width // 2, self.screen_height // 2 + 70, center=True)


    def scroll_view(self, direction):
        """Scrolls the view left or right, respecting boundaries."""
        self.scroll_offset += direction * self.SCROLL_SPEED
        self.scroll_offset = max(0, self.scroll_offset)
        list_width = self.total_nodes * (self.NODE_WIDTH + self.ARROW_LENGTH) - self.ARROW_LENGTH if self.total_nodes > 0 else 0
        max_scroll = max(0, list_width - self.screen_width + 100)
        self.scroll_offset = min(self.scroll_offset, max_scroll)


    def handle_action(self, action_type):
        """Handles game logic when a button is pressed or key is used."""
        if self.game_over or not self.linked_list.current:
            return

        current_node = self.linked_list.current
        correctness = current_node.is_correct
        nodes_before_action = self.total_nodes

        # --- Perform Action & Update State ---
        if action_type == 'delete':
            if not correctness:
                self.score += 1
                self.feedback_message = "Correct! Deleted wrong answer."
                self.feedback_icon = "✅"
                self.feedback_color = self.GREEN
            else:
                self.feedback_message = "Oops! Deleted correct answer."
                self.feedback_icon = "❌"
                self.feedback_color = self.RED
            self.linked_list.delete_current_node()
            self.total_nodes -= 1 # Update node count

        elif action_type == 'next':
            self.feedback_message = "Skipped to next question."
            self.feedback_icon = "⏭️"
            self.feedback_color = self.DARK_GRAY
            self.linked_list.move_right()

        elif action_type == 'confirm':
            if correctness:
                self.score += 1
                self.feedback_message = "Correct! Confirmed right answer."
                self.feedback_icon = "✅"
                self.feedback_color = self.GREEN
                self.linked_list.move_right()
            else:
                self.feedback_message = f"Incorrect! Answer was '{current_node.answer}'."
                self.feedback_icon = "❌"
                self.feedback_color = self.RED
                self.linked_list.move_right()

        self.feedback_timer = 150 # Show feedback

        # --- Post-Action Updates ---
        # Auto-scroll if the current node changed or if a node was deleted
        if self.linked_list.current != current_node or self.total_nodes < nodes_before_action:
             self.auto_scroll_to_current()

        # --- Check for Game Over Condition ---
        # Game ends if the list head becomes None (empty list)
        if self.linked_list.head is None:
            self.game_over = True
        # Or if the current pointer becomes None *after* a move action (meaning we moved off the end)
        elif self.linked_list.current is None and self.linked_list.head is not None and action_type != 'delete':
            self.game_over = True


    def auto_scroll_to_current(self):
        """Adjusts scroll_offset to try and keep the current node centered, if possible."""
        if not self.linked_list.current:
             if self.total_nodes == 0:
                 self.scroll_offset = 0
             return

        node_index = 0
        temp = self.linked_list.head
        while temp and temp != self.linked_list.current:
            node_index += 1
            temp = temp.next
        if temp is None: return

        target_center_x_on_screen = self.screen_width // 2
        node_center_x_abs = 100 + node_index * (self.NODE_WIDTH + self.ARROW_LENGTH) + self.NODE_WIDTH // 2
        target_scroll_offset = node_center_x_abs - target_center_x_on_screen

        list_width = self.total_nodes * (self.NODE_WIDTH + self.ARROW_LENGTH) - self.ARROW_LENGTH if self.total_nodes > 0 else 0
        max_scroll = max(0, list_width - self.screen_width + 100)
        target_scroll_offset = max(0, min(target_scroll_offset, max_scroll))
        self.scroll_offset = target_scroll_offset


    def handle_input(self):
        """Processes Pygame events."""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False # Signal to exit game loop

            if self.game_over:
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.__init__(self.screen_width, self.screen_height) # Restart
                    elif event.key == K_q:
                        return False # Quit
            else: # Input only handled if game is not over
                if event.type == MOUSEBUTTONDOWN:
                    if self.delete_button.collidepoint(event.pos):
                        self.handle_action('delete')
                    elif self.next_button.collidepoint(event.pos):
                        self.handle_action('next')
                    elif self.confirm_button.collidepoint(event.pos):
                        self.handle_action('confirm')

                    if event.button == 4: self.scroll_view(-1) # Scroll up
                    elif event.button == 5: self.scroll_view(1)  # Scroll down

                if event.type == KEYDOWN:
                    if event.key == K_LEFT: self.scroll_view(-1)
                    elif event.key == K_RIGHT: self.scroll_view(1)
                    elif event.key == K_1 or event.key == K_KP1: self.handle_action('delete')
                    elif event.key == K_2 or event.key == K_KP2: self.handle_action('next')
                    elif event.key == K_3 or event.key == K_KP3: self.handle_action('confirm')
        return True # Signal to continue game loop


    def run_game(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_input()
            if not running: break

            # Check for game over if list started empty (or became empty outside handle_action)
            if self.total_nodes == 0 and not self.game_over and self.linked_list.head is None:
                 self.game_over = True
                 if not self.feedback_message: # Avoid overwriting load error messages
                      self.feedback_message = "No questions available."
                      self.feedback_icon = "🤷"
                      self.feedback_color = self.DARK_GRAY
                      self.feedback_timer = 300

            # Draw frame
            self.draw_gradient_background()
            if not self.game_over:
                 self.draw_list()
                 self.draw_header_footer() # Draws feedback in correct spot now
                 self.draw_buttons()
                 self.draw_scroll_indicators()
            else:
                 self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# --- Main Execution ---
if __name__ == '__main__':
    print("Running Trivia Trek GUI directly (Final Version)...")
    game_gui = TriviaGameGUI()
    game_gui.run_game()

# --- END OF FILE ui/gui.py ---