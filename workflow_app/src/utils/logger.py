import logging

logging.basicConfig(
    filename="workflow.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)

logger = logging.getLogger("workflow")
