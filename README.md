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