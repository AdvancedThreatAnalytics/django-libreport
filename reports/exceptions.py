class ReportSkipped(Exception):
    """Skip this report"""
    def __init__(self, reason="no data"):
        super(ReportSkipped, self).__init__()
        self.reason = reason
