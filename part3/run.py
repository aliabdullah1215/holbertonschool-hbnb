from app import create_app
from app.api.v1 import api as api_v1

app = create_app()

# Register API v1
api_v1.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
