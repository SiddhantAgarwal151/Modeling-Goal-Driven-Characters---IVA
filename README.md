# **Modeling Goal-Driven Characters - IVA**  

An interactive storytelling system where characters evolve based on beliefs, emotions, and AI-driven responses.  

## **Setup & Run**  
1. **Clone the repo**  
   ```bash
   git clone https://github.com/SiddhantAgarwal151/Modeling-Goal-Driven-Characters---IVA.git  
   cd Modeling-Goal-Driven-Characters---IVA
   ```  
2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```  
3. **Set up API Key**  
   - Create a `.env` file:  
     ```bash
     OPENAI_API_KEY=your_api_key_here
     ```  
4. **Run the script**  
   ```bash
   python main.py
   ```  

## **How It Works**  
- Characters update **beliefs & emotions** dynamically.  
- GPT-4 **generates story responses** based on events.  
- Events like **confrontations & malfunctions** alter trust & suspicion.  

## **Troubleshooting**  
- **API errors?** Ensure `.env` has a valid OpenAI API key.  
- **Install issues?** Run `pip install openai python-dotenv`.  

🚀 **Engage in AI-driven storytelling!**
