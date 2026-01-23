// component will load the story for the user and display on the page
import { useState, useEffect } from "react";

//Error found while testing frontend - useParams is not a function at StoryLoader
// resolution - replacing react with react-router-dom
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import LoadingStatus from "./LoadingStatus.jsx";
// importing StoryGame
import StoryGame from "./StoryGame.jsx";
import { API_BASE_URL } from "../util.js";

// here we are trying to fetch story id from the browser url to fetch the story from the backend
//  /frontend_link/story/story_id

function StoryLoader() {
  const { id } = useParams();
  const navigate = useNavigate(); //for navigating to other pages when router is set

  // useState(<current state of the variable>)
  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // using useEffect as - as soon as page is rendered, the loadStory func will be called when id changes inthe browser

  useEffect(() => {
    loadStory(id);
  }, [id]);

  // Async function to load the stories
  const loadStory = async (storyId) => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(
        `${API_BASE_URL}/stories/${storyId}/complete`,
      );
      setStory(response.data);
      setLoading(false);
    } catch (err) {
      if (err.response?.status === 404) {
        setError("Story is not found.");
      } else {
        setError("Failed to load story");
      }
    } finally {
      setLoading(false);
    }
  };

  // func to create new story - navigating back to home page
  const createNewStory = () => {
    navigate("/");
  };

  // if loading - current state is true, then loading status will be rendered with theme

  if (loading) {
    return <LoadingStatus theme={"story"} />;
  }

  if (error) {
    return (
      <div className="story-loader">
        <div className="error-message">
          <h2>Story Not Found</h2>
          <p>{error}</p>
          {/* if story generation failed, we will allow user to go back to page for new story generation  */}
          <button onClick={createNewStory}>Go to Story Generator</button>
        </div>
      </div>
    );
  }

  if (story) {
    return (
      <div className="story-loader">
        {/* for rendering the story from -StoryGame component-  */}

        <StoryGame story={story} onNewStory={createNewStory} />
      </div>
    );
  }
}

export default StoryLoader;
