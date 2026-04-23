"""
models.py
Defines the Job hierarchy (parent + child classes).
Polymorphism: each subclass implements its own execute().
"""


class Job:

    """Parent/base class shared by all job types."""

    def __init__(self, job_id: int, description: str) -> None:

        self.job_id = job_id

        self.description = description

        self.status = "pending"


    def execute(self) -> None:

        """Must be overridden by subclasses."""

        raise NotImplementedError("Each job must implement its own execution logic.")


    def mark_done(self) -> None:

        self.status = "completed"


    def __repr__(self) -> str:

        return f"<Job id={self.job_id} status={self.status}desc='{self.description}'>"



class EmailJob(Job):

    """Child class: sends an email."""

    def __init__(self, job_id: int, recipient: str) -> None:

        # super() calls parent constructor (DRY)

        super().__init__(job_id, f"Send email to {recipient}")

        self.recipient = recipient


    def execute(self) -> None:

        print(f"Sending email to {self.recipient}...")

        # FIX (models.py): removed self.mark_done() here.
        # Previously mark_done() set job.status="completed" inside execute(),
        # so update_status() in executor.py searched the wrong bucket and
        # added a duplicate — causing Pending:4, Completed:4 in the summary.
        # Status is now managed exclusively by TaskManager.update_status().



class DataProcessingJob(Job):

    """Child class: processes a dataset."""

    def __init__(self, job_id: int, dataset: str) -> None:

        super().__init__(job_id, f"Process dataset {dataset}")

        self.dataset = dataset


    def execute(self) -> None:

        print(f"Processing dataset {self.dataset}...")

        # FIX (models.py): removed self.mark_done() here — same reason as EmailJob above.


# Activity 2: PriorityJob - Add Job Prioritisation

class PriorityJob(Job):
    PRIORITY_LEVELS = ["low", "medium", "high", "critical"]

    def __init__(self, job_id, description, priority="medium"):
        super().__init__(job_id, description)
        if priority not in self.PRIORITY_LEVELS:
            raise ValueError(f"Invalid priority. Choose from: {self.PRIORITY_LEVELS}")
        self.__priority = priority  # private attribute (encapsulation)

    def get_priority(self):
        return self.__priority

    def execute(self):
        print(f"[PriorityJob] Executing job {self.job_id} "
              f"with priority '{self.__priority}': {self.description}")
        self.mark_done()