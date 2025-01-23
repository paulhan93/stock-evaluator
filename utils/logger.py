class StockAnalysisLogger:
    def __init__(self, original_stdout, file):
        self.terminal = original_stdout
        self.file = file

    def write(self, message):
        self.file.write(message)
        self.terminal.write(message)

    def flush(self):
        self.file.flush()
        self.terminal.flush() 