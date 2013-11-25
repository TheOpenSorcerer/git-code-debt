from git_code_debt.metric import Metric

class DiffParserBase(object):
    """Generates metrics from git show"""
    # Specify __metric__ = False to not be included
    __metric__ = False

    def get_metrics_from_stat(self, file_diff_stats):
        """Implement me to yield Metric objects from the input list of
        FileStat objects.

        Args:
            file_diff_stats - list of FileDiffStat objects

        Returns:
           generator of Metric objects
        """
        raise NotImplementedError

    def get_possible_metric_ids(self):
        raise NotImplementedError

class SimpleLineCounterBase(DiffParserBase):
    """Simple counter for various file types and line types."""
    __metric__ = False

    def get_metrics_from_stat(self, file_diff_stats):
        metric_value = 0

        for file_diff_stat in file_diff_stats:
            if self.should_include_file(file_diff_stat):
                for line in file_diff_stat.lines_added:
                    if self.line_matches_metric(line, file_diff_stat):
                        metric_value += 1
                for line in file_diff_stat.lines_removed:
                    if self.line_matches_metric(line, file_diff_stat):
                        metric_value -= 1

        yield Metric(self.metric_name, metric_value)

    def get_possible_metric_ids(self):
        return [self.metric_name]

    @property
    def metric_name(self):
        """Override me or make a class-level metric_name attribute to set the
        metric name.
        """
        return self.__class__.__name__

    def should_include_file(self, file_diff_stat):
        """Implement me to return whether a filename should be included.

        Args:
            file_diff_stat - FileDiffStat object
        """
        return True

    def line_matches_metric(self, line, file_diff_stat):
        """Implement me to return whether a line matches the metric.

        Args:
            line - Line in the file
            file_diff_stat - FileDiffStat object
        """
        raise NotImplementedError
