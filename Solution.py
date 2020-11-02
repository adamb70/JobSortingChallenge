import unittest


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

            job, dependency = line.split('=>')
            self.job_mapping[job.strip()] = dependency.strip() if dependency else None
        return self.job_mapping

    def load_jobs_file(self, filepath):
        with open(filepath, 'r') as infile:
            self.load_jobs(infile.read())
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


class SolutionTest(unittest.TestCase):
    def test_loading(self):
        registry = JobRegistry()
        jobs = registry.load_jobs("""
        a =>
        b => c
        c =>
        """)
        self.assertEqual(jobs, {'a': None, 'b': 'c', 'c': None})

    def test_loading_file(self):
        registry = JobRegistry()
        jobs = registry.load_jobs_file('fail_case_2.txt')
        self.assertEqual(jobs, {'a': None, 'b': 'c', 'c': 'f', 'd': 'a', 'e': None, 'f': 'b'})

        registry = JobRegistry()
        jobs = registry.load_jobs_file('pass_case_3.txt')
        self.assertEqual(jobs, {'a': None, 'b': 'c', 'c': 'f', 'd': 'a', 'e': 'b', 'f': None})

    def test_sort_jobs_passes(self):
        registry = JobRegistry()
        registry.load_jobs_file('pass_case_1.txt')
        sorted_jobs = registry.sort_jobs()
        self.assertEqual(sorted_jobs, ['a', 'b', 'c'])

        registry = JobRegistry()
        registry.load_jobs_file('pass_case_2.txt')
        sorted_jobs = registry.sort_jobs()
        self.assertEqual(sorted_jobs, ['a', 'c', 'b'])

        registry = JobRegistry()
        registry.load_jobs_file('pass_case_3.txt')
        sorted_jobs = registry.sort_jobs()
        self.assertEqual(sorted_jobs, ['a', 'f', 'c', 'b', 'd', 'e'])

    def test_sort_jobs_fails(self):
        registry = JobRegistry()
        registry.load_jobs_file('fail_case_1.txt')
        with self.assertRaisesRegex(Exception, "Jobs can't depend on themselves!"):
            registry.sort_jobs()

        registry = JobRegistry()
        registry.load_jobs_file('fail_case_2.txt')
        with self.assertRaisesRegex(Exception, "Jobs can't have circular dependencies!"):
            registry.sort_jobs()


if __name__ == '__main__':
    unittest.main()
