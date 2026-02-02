# Story Weave
<img width="1376" height="768" alt="Gemini_Generated_Image_qoscltqoscltqosc" src="https://github.com/user-attachments/assets/a53e9dff-3267-4b4e-9fdf-7ccf80a86a30" />


**Story Weaver** is a dynamic, AI-powered storytelling platform that allows users to co-create immersive narratives. By simply providing a theme, users are dropped into a branching storyline where every decision shapes a unique path toward multiple potential conclusions.


## How It Works

The application uses Generative AI to create a "Choose Your Own Adventure" experience in real-time. It takes a user-defined theme and generates a starting scenario with multiple choices. Every selection sends a new prompt to the AI, ensuring that every playthrough is a completely original journey.

### Key Features
* **Theme Based Generation:** Create stories about anything from *Cyberpunk Heists* to *Deep Sea Exploration*.
* **Dynamic Decision Making:** Your choices directly impact the plot, character survival, and the world state.
* **Immersive Pixel Art UI:** A nostalgic, high-fantasy aesthetic designed to spark the imagination.
* **Multiple Endings:** Fail, sacrifice yourself for the greater good, or achieve a legendary victory.


## Tech Stack

* **Frontend:** React (Hooks, Functional Components, Custom CSS for Pixel Art styling)
* **Backend:** FastAPI (Python-based, high-performance async processing)
* **AI Integration:** Google Gemini API (Natural Language Generation for story branching)

---

## 📖 Workflow Explanation

1. **The Home Page** -> The landing page invites you to "Weave your Story" with a clean, thematic pixel-art design.  
   <img width="959" height="442" alt="1 HomePage" src="https://github.com/user-attachments/assets/a30aa2b7-de66-4387-9f6a-672af58c0575" />


2. **Defining the Theme** -> Enter a prompt (e.g., "Space Ship") to set the creative boundaries for the AI engine.  
   <img width="959" height="443" alt="2 AddingThemeForStory" src="https://github.com/user-attachments/assets/e6b8d0c1-b4ec-489f-835b-5f8c4919ef8c" />


3. **Real Time AI Generation** -> The FastAPI backend triggers the Gemini API to craft a custom narrative starting point.  
   <img width="959" height="442" alt="3 GeneratingStoryLoading" src="https://github.com/user-attachments/assets/fac89c94-f534-4209-b4c7-5dba87b96e61" />


4. **Interactive Choice System** -> Users are presented with the initial scenario and three distinct paths to choose from.  
   <img width="959" height="443" alt="4 GeneratedOptionsFirstChoice" src="https://github.com/user-attachments/assets/8b14f92e-af2b-465b-b47b-edbda312fe55" />


5. **Branching Narratives** -> Each choice leads to deeper lore, evolving the story based on your specific decisions.  
   <img width="959" height="441" alt="5 GeneratedOptionsSecondChoice" src="https://github.com/user-attachments/assets/d4f85437-235b-4f53-a057-02b71702e6e2" />


6. **Rising Stakes** -> The tension builds as the AI generates a climax based on your previous survival strategies.  
   <img width="959" height="442" alt="6 GeneratedOptionsThirdChoice" src="https://github.com/user-attachments/assets/c4ff0e8e-617c-452a-b1f4-68bee48431f3" />


7. **The Final Outcome** -> Whether it is a tragic sacrifice or a "Winning Ending," the conclusion is a direct result of your journey.  
   <img width="959" height="446" alt="7 StoryEnding" src="https://github.com/user-attachments/assets/cb002db4-a106-45db-be80-b1c6d8281826" />
   <img width="959" height="442" alt="8 StoryWinningEnding" src="https://github.com/user-attachments/assets/9dfb1fe9-16a1-412d-99ac-6b37a209d3db" />


---

## Engineering Insights

Through the development of this project, I gained deep technical experience in:

* **Prompt Engineering:** I mastered structuring LLM prompts to return consistent, JSON parsable story segments while maintaining narrative continuity.
* **Async Full-Stack Architecture:** Implemented **FastAPI** to handle the inherent latency of AI generation, ensuring the React frontend remains responsive and fluid.
* **Stateful Storytelling:** Developed complex logic to track user progress and "state," ensuring that the AI context remains relevant to previous choices.
* **Modern API Integration:** Gained hands-on experience connecting a JavaScript based UI to a Python-based AI backend, optimizing data flow and error handling.
* **UX for Generative Tech:** Created intuitive feedback loops (loading states and transitions) to manage the user experience during real time content creation.

---

### 🔗 Explore the Code
Check out the full repository and implementation details here:  
[GitHub: Story-Weave](https://github.com/AK-Amit-Kumar/Story-Weave)
