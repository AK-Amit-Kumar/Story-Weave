import { useState, useEffect } from "react";

// defining all the necessary variable and their inital states

function StoryGame({ story, onNewStory }) {
  const [currentNodeId, setCurrentNodeId] = useState(null);
  const [currentNode, setCurrentNode] = useState(null);
  const [options, setOptions] = useState(null);
  const [isEnding, setIsEnding] = useState(null);
  const [isWinningEnding, setIsWinningEnding] = useState(null);

  //  ****** setting up all the values needed for further processing *****

  // using the story parameter passed to the func and fetching the root node id and then
  // setting the current node id as recieved root node id

  // dependency = [story]  - when story variable value changes, useEffect is rerendered based on that value
  // 1st useEffect logic
  useEffect(() => {
    if (story && story.root_node) {
      const rootNodeId = story.root_node.id;
      setCurrentNodeId(rootNodeId);
    }
  }, [story]);

  // following will run when node id changes and will give us options for the story
  // 2nd UseEffect Logic
  useEffect(() => {
    if (currentNodeId && story && story.all_nodes) {
      const node = story.all_nodes[currentNodeId]; // if_cond is true, then we are fetchinf all the node dtails for current node id

      // setting the variable states based on value of node
      setCurrentNode(node);
      setIsEnding(node.is_ending);
      setIsWinningEnding(node.is_winning_ending);

      //logic for considering the nodes which is not last last(ending) node and  having child nodes as options
      if (!node.is_ending && node.options && node.options.length > 0) {
        setOptions(node.options);
      } else {
        setOptions([]);
      }
    }
  }, [currentNodeId, story]);

  // logic to choose the child nodes as options and then it will rendered based on 2nd useEffect logic
  const chooseOption = (optionId) => {
    setCurrentNodeId(optionId);
  };

  //logic to restart the story creation based on 2nd useEffect logic
  const restartStory = () => {
    if (story && story.root_node) {
      setCurrentNodeId(story.root_node.id);
    }
  };

  // setting up UI for StoryGame component
  return (
    <div className="story-game">
      {/* header element of the story  */}
      <header className="story-header">
        <h2>{story.title}</h2>
      </header>

      <div className="story-content">
        {currenNode && (
          <div className="story-node">
            <p>{currentNode.content}</p>

            {/* if the node is ending node  */}
            {isEnding ? (
              <div className="story-ending">
                <h3>{isWinningEnding ? "Congratulations" : "The End"}</h3>
                {isWinningEnding
                  ? "You reached a winning ending"
                  : "Your adventure of weaving a story is ended."}
              </div>
            ) : (
              <div className="story-options">
                <h3>What will you do?</h3>
                <div className="options-list">
                  {options.map((option, index) => {
                    return (
                      <button
                        key={index}
                        onClick={() => chooseOption(option.node_id)}
                        className="option-btn"
                      >
                        {option.text}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}

        {/* button for story controls  */}
        <div className="story-controls">
          <button onClick={restartStory} className="reset-btn">
            Restart Story
          </button>
        </div>

        {/* getting this button only when there is new story  */}
        {onNewStory && (
          <button onClick={onNewStory} className="new-story-btn">
            New Story
          </button>
        )}
      </div>
    </div>
  );
}

export default StoryGame; //to be used in Story Loader component
