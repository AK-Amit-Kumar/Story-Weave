// component to get the input for our theme
import { useState } from "react";

// onsubmit function will be called later 
function ThemeInput({onSubmit}) {
    const [theme,setTheme] = useState("")
    const [error,setError] = useState("")

    const handleSubmit = (e) => {
        e.preventDefault();   // to avoid default form submission

        // if nothing is sent as theme apart from empty string 
        if(!theme.trim()) {
            setError("Please enter a theme name");
            return
        }

        onSubmit(theme);
    }
    return <div className="theme-input-container">
        <h2>Weave your Story</h2>
        <p>Enter a theme for your interactive story</p>

        {/* creating form fields for getting theme value */}
        <form onSubmit={handleSubmit}>
            <div className="input-group">
                <input 
                    type="text" 
                    value={theme}
                    onChange={(e)=>setTheme(e.target.value)}
                    placeholder="Enter a theme (e.g. pirates, space)"
                    // if there is error, input box will be highlighted
                    className={error ? 'error' : ''}
                />
                {error && <p className="error-text">{error}</p>}
            </div>
            <button type="submit" className='generate-btn'>
                Generate Story 
            </button>
        </form>
    </div>
}

export default ThemeInput