import os
from statistic import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=port)
