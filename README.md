# gen-slater

Have you ever wanted to correctly communicate with a friend or family member of a different generation, and thus uses incomprehensible slang? Now that is finally possible with GEN-SLATER. With an API key, this application uses a next-word-prediction-model to consistently translate your slang to slang of another generation.

## Installation and Initialization

There are some very simple steps in order for you to be able to run this application yourself.

1. Clone git repository:
   ```bash
   git clone https://github.com/rrocketmann/gen-slater
   cd gen-slater
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. Run application:
   ```bash
   flask run
   ```

## Thank You!

Please star this repo if you like it and find it useful. 

**Live Demo:** [gen-slater.onrender.com](https://gen-slater.onrender.com) (Note: May sleep after inactivity on free tier)
