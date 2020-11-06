import unittest

from Solution import JobLoader, JobSorter


class JobLoaderTest(unittest.TestCase):
    def test_loading(self):
        loader = JobLoader()
        jobs = loader.load_jobs("""
        a =>
        b => c
        c =>
        """)
        self.assertEqual(jobs, {'a': None, 'b': 'c', 'c': None})

    def test_loading_file(self):
        loader = JobLoader()
        jobs = loader.load_jobs_file('fail_case_2.txt')
        self.assertEqual(jobs, {'a': None, 'b': 'c', 'c': 'f', 'd': 'a', 'e': None, 'f': 'b'})

        jobs = loader.load_jobs_file('pass_case_3.txt')
        self.assertEqual(jobs, {'a': None, 'b': 'c', 'c': 'f', 'd': 'a', 'e': 'b', 'f': None})


class JobSorterTest(unittest.TestCase):
    def test_check_job(self):
        sorter = JobSorter()
        sorter.job_mapping = {'a': None, 'b': 'c', 'c': 'f', 'd': 'a', 'e': 'b', 'f': None}

        sorter.check_job('a')
        self.assertEqual(sorter.sorted_jobs, ['a'])

        sorter.sorted_jobs = []  # reset
        sorter.check_job('b')
        self.assertEqual(sorter.sorted_jobs, ['f', 'c', 'b'])

        sorter.sorted_jobs = []  # reset
        sorter.check_job('e')
        self.assertEqual(sorter.sorted_jobs, ['f', 'c', 'b', 'e'])

    def test_sort_jobs_passes(self):
        loader = JobLoader()
        sorter = JobSorter()
        loader.load_jobs_file('pass_case_1.txt')
        sorted_jobs = sorter.sort_jobs(loader.job_mapping)
        self.assertEqual(sorted_jobs, ['a', 'b', 'c'])

        loader.load_jobs_file('pass_case_2.txt')
        sorted_jobs = sorter.sort_jobs(loader.job_mapping)
        self.assertEqual(sorted_jobs, ['a', 'c', 'b'])

        loader.load_jobs_file('pass_case_3.txt')
        sorted_jobs = sorter.sort_jobs(loader.job_mapping)
        self.assertEqual(sorted_jobs, ['a', 'f', 'c', 'b', 'd', 'e'])

    def test_sort_jobs_fails(self):
        loader = JobLoader()
        sorter = JobSorter()
        loader.load_jobs_file('fail_case_1.txt')
        with self.assertRaisesRegex(Exception, "Jobs can't depend on themselves!"):
            sorter.sort_jobs(loader.job_mapping)

        loader.load_jobs_file('fail_case_2.txt')
        with self.assertRaisesRegex(Exception, "Jobs can't have circular dependencies!"):
            sorter.sort_jobs(loader.job_mapping)

