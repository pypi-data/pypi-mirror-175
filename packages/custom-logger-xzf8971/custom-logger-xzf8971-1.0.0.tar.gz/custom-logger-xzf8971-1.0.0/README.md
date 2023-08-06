# custom-logger-xzf8971
Just a very simple wrapper to configure a thread safe logger.

# Usage
<font color='red'>The logger_name must be exclusive!</font>
```python
from custom_logger import CustomLoggerWrapper

loggerWrapper = CustomLoggerWrapper(logger_name="example_logger" logger_level=logging.INFO, logger_propagate=False, logger_fmt="%(asctime)s - %(levelname)s - %(message)s", log_filename="mylog.log")
loggerWrapper.InitLogger()
logger = loggerWrapper.GetInitedLogger()
logger.info("example")
```