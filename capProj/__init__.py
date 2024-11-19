import os

from flask import Flask

from openai import OpenAI


def createApp(testConfig=None):
    #configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'capProject.sqlite'),

    )

    if testConfig is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(testConfig)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    
    @app.route('/ta')
    def chat():
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "you are a helpful assistant."},
                {
                    "role": "user",
                    "content": "Explain how recursion works."
                }
            ]

        )
        
        processed = completion.choices[0].message
        return str(processed)
    

    from . import db
    db.initApp(app)

    return app  