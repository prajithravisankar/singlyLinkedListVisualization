### **Project Overview**

A **Pygame-based visualization** of a **singly linked list** where each node contains a **trivia question**. The player must navigate through the list, deciding whether to **delete incorrect answers** or **confirm correct ones**, reinforcing **data structure concepts** while testing general knowledge.

### **Core Learning Objectives**

✅ **Singly Linked List Operations** (Traversal, Deletion)

✅ **Interactive Data Structure Visualization** (Pygame)

✅ **Game Logic & State Management** (Score Tracking, Node Navigation)

---

## **Technical Implementation**

### **1. Data Structures Used**

- **Singly Linked List** (Nodes store trivia questions, answers, and correctness)
- **Game State Manager** (Tracks score, current node, and game progress)

### **2. Features**

✔ **Visual Node Representation** (Rectangles with text, connected by arrows)

✔ **Three Actions**:

- **Move Right** (Traverse to next node)
- **Delete Node** (If answer is wrong, gain points)
- **Confirm Correct** (If answer is right, gain points)
✔ **Dynamic Feedback**:
- Shows whether the player made the right choice
- Updates score in real-time
✔ **Endgame Summary**:
- Displays missed questions, correct choices, and final score

### **3. Game Logic Flow**

1. **Initialize** the linked list with trivia questions.
2. **Display** the current node’s question and answer.
3. **Player chooses an action**:
    - **Delete Node** → If answer is wrong → **+1 point**
    - **Confirm Correct** → If answer is right → **+1 point**
    - **Move Right** → Skip (no points, proceed to next node)
4. **Repeat** until the end of the list.
5. **Show results** (Score breakdown, missed questions).

---

### **Example Scenario**

| **Node** | **Question** | **Answer** | **Correct?** | **Player Action** | **Outcome** |
| --- | --- | --- | --- | --- | --- |
| 1 | Who is the current US president? | Kamala Harris | ❌ | **🗑️ Delete** | +1 point |
| 2 | Fastest land animal? | Cheetah | ✅ | **✓ Correct** | +1 point |
| 3 | Largest planet? | Jupiter | ✅ | **→ Move Right** | No points (missed opportunity cannot go back because singly linked list) |

---

## **Phase 0: Project & Environment Setup**

## **Phase 0: Project & Environment Setup**

- [x]  Create `trivia_game/` folder.
- [x]  Set up a virtual environment (`python -m venv venv`).
- [x]  Install dependencies:
    - [x]  `pip install pygame`
    - [x]  `pip install pytest`
- [x]  Create project file structure as shown.
- [x]  Initialize Git repository (optional but recommended).
- [x]  Create empty `requirements.txt` (`pip freeze > requirements.txt`).

## **Phase 1: Core Data Structures (Node & Linked List Classes)**

### 📚 Study Reminder Before Phase 1

- [x]  Review **classes, attributes, constructors** in Python.
- [ ]  Review **basic linked lists** (singly linked).

---

### 🧩 Main Todo 1.1: Node Class (core/node.py)

- [x]  **Subtodo: Signature**
    - Write constructor signature:
    
    ```python
    # Node(question: str, answer: str, is_correct: bool) -> Node
    
    ```
    
- [x]  **Subtodo: Purpose**
    - Describe: "Represents a trivia question node with data and next pointer."
- [x]  **Subtodo: Stub**
    - Create `Node` class with attributes set to dummy values.
- [x]  **Subtodo: Unit Test (tests/test_node.py)**
    - Test node creation.
- [x]  **Subtodo: Run Test**
    - Tests should fail.
- [x]  **Subtodo: Implement Node Class**
    - Real code to initialize attributes: `question`, `answer`, `is_correct`, `next = None`.

---

## **Phase 2: CLI User Interface**

## **Phase 3: CLI Testing Improvement**

## **Phase 4: Visualization with Pygame (ui/pygame_ui.py)**

## **Phase 5: Final Polish**