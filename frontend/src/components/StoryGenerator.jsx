import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import ThemeInput from "./ThemeInput.jsx";
import LoadingStatus from "./LoadingStatus.jsx";
import { API_BASE_URL } from "../util.js";

// for submitting the theme to backend
//responsible for polling the endpoint
// this component will be added as one of the route in App.jsx

function StoryGenerator() {
  // setting up the states for to be used in useEffect Hooks
  const navigate = useNavigate();
  const [theme, setTheme] = useState("");
  const [jobId, setJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // functionality using useEffect Hooks
  useEffect(() => {
    let pollInterval;

    if (jobId && jobStatus === "processing") {
      //calling pollJobStatus in intervals - 5 seconds
      pollInterval = setInterval(() => {
        pollJobStatus(jobId);
      }, 5000);
    }

    // returning in order to close the interval
    return () => {
      if (pollInterval) {
        clearInterval(pollInterval);
      }
    };
  }, [jobId, jobStatus]);

  // function to gennerate the story
  const generateStory = async (theme) => {
    setLoading(true);
    setError(null);
    setTheme(theme);

    try {
      // sending the request to create the story
      const response = await axios.post(`${API_BASE_URL}/stories/create`, {
        theme,
      });
      const { job_id, status } = response.data; // destructuring data to get necessary information

      // setting jobid and jobstatus state for that particular job based on data got in as response
      setJobId(job_id);
      setJobStatus(status);

      // calling the function to check if the job is ready
      // will add logic of useEffect which will keep calling this constantly till the job is done

      pollJobStatus(job_id);
    } catch (e) {
      setLoading(false);
      setError(`Failed to generate story: ${e.message}`);
    }
  };

  // function to poll Job Status
  // if the status is pending or processing, it will keep on running below func until we get -completed- or -failed-
  const pollJobStatus = async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/jobs/${id}`);
      const { status, story_id, error: jobError } = response.data; //destructuring data
      setJobStatus(status);

      if (status === "completed" && story_id) {
        fetchStory(story_id);
      } else if (status === "failed" || jobError) {
        setError(jobError || "Failed to generate story");
        setLoading(false);
      }
    } catch (e) {
      if (e.response?.status !== 404) {
        setError(`Failed to check story status: ${e.message}`);
        setLoading(false);
      }
    }
  };
  // function is called as soon as job is finished - redirecting to the completion page after job success

  const fetchStory = async (id) => {
    try {
      setLoading(false);
      setJobStatus("completed");
      navigate(`/story/${id}`);
    } catch (e) {
      setError(`Failed to load the story: ${e.message}`);
      setLoading(false);
    }
  };

  // fucntion to reset the above dedfined state forms - when error encoutered, we will reset the states
  const reset = () => {
    setJobId(null);
    setJobStatus(null);
    setError(null);
    setTheme("");
    setLoading(false);
  };

  return (
    <div className="story-generator">
      {/* error handling */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={reset}>Try Again</button>
        </div>
      )}

      {/* inputs for the Theme  */}
      {!jobId && !error && !loading && <ThemeInput onSubmit={generateStory} />}

      {/* loading status  */}
      {loading && <LoadingStatus theme={theme} />}
    </div>
  );
}

export default StoryGenerator;
