
class JobRegistry:
    def __init__(self):
        self.sorted_jobs = []
        self.job_mapping = {}

    def load_jobs(self, jobstring):
        """ Assume jobstring is given as `job => dependency` on separate lines."""
        for line in jobstring.splitlines():
            line = line.strip()
            if not line:
                # Ignore blank lines
                continue

            job, dependency = line.split(' => ')
            self.job_mapping[job] = dependency if dependency else None
        return self.job_mapping

    def check_job(self, job, visited=None):
        dep = self.job_mapping[job]

        if visited:
            # We are looking recursively, check for circular dependencies
            if job in visited:
                raise Exception("Jobs can't have circular dependencies!")
            visited.append(job)
        else:
            visited = [job]

        if not dep or dep in self.sorted_jobs:
            # This job has no dependency, or dependency is already sorted,
            # add visited jobs to the output list in reverse order
            self.sorted_jobs.extend(reversed(visited))
            return

        if dep == job:
            raise Exception("Jobs can't depend on themselves!")

        return self.check_job(dep, visited)

    def sort_jobs(self):
        for job in self.job_mapping.keys():
            if job not in self.sorted_jobs:
                self.check_job(job)

        return self.sorted_jobs

