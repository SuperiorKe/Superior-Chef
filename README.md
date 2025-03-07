# Pantry Chef 🍳

![Pantry Chef Logo](https://via.placeholder.com/800x200?text=Pantry+Chef)

Pantry Chef is a smart web application that helps you discover delicious recipes based on ingredients you already have in your kitchen. No more food waste or last-minute grocery store trips!

## ✨ Features

- **Ingredient-Based Search**: Enter ingredients you have on hand
- **Smart Recipe Matching**: Get recipes that use what you already have
- **Detailed Instructions**: Clear, step-by-step cooking directions
- **Recipe Alternatives**: Don't like a suggestion? Get another with one click
- **Responsive Design**: Works on desktop and mobile devices
- **Print Functionality**: Save or print recipes for offline use

## 🛠️ Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite (local recipes), Spoonacular API (extended recipe database)
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Icons**: Font Awesome

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- pip (Python package manager)
- Git

## 🚀 Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/SuperiorKe/Superior-chef.git
   cd pantry-chef
   ```

2. **Create a virtual environment**:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Spoonacular API key**:
   - Sign up for a free API key at [Spoonacular API](https://spoonacular.com/food-api)
   - Create a `.env` file in the project root
   - Add your API key to the file:
     ```
     SPOONACULAR_API_KEY=your_api_key_here
     ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   - Open your browser and navigate to `http://localhost:5000`

## 🧑‍🍳 How to Use

1. **Enter your ingredients**:
   - Type the ingredients you have in your kitchen, separated by commas
   - Example: "eggs, avocado, beans, onions, tomatoes"

2. **Get recipe recommendations**:
   - Click "Find Recipes" to see what you can make
   - The app will search for recipes that use at least 60% of your ingredients

3. **View recipe details**:
   - See the recipe name, ingredients list, and cooking instructions
   - If available, a photo of the finished dish will be displayed

4. **Try alternative recipes**:
   - If you don't like the suggested recipe, click "Try Another Recipe"
   - The app will suggest a different recipe using your ingredients

5. **Save your recipe**:
   - Use the "Print Recipe" button to print or save the recipe as a PDF

## 📱 Screenshots

![Home Screen](C:\Users\kevma\Desktop\Cursor-Demo\home.png)
![Recipe Results](C:\Users\kevma\Desktop\Cursor-Demo\Recipe.png)

## 🔄 API Integration

Pantry Chef uses the Spoonacular API to access thousands of recipes. The application:
- Searches for recipes based on available ingredients
- Retrieves detailed cooking instructions
- Falls back to local database recipes if API limits are reached

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin new-feature`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Spoonacular API](https://spoonacular.com/food-api) for providing recipe data
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Font Awesome](https://fontawesome.com/) for icons
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 📞 Contact

If you have any questions or suggestions, please open an issue or contact the repository owner.

---

Made with ❤️ by Kenn