FROM python:3

ADD ComputeMetrics.py /
RUN pip install pandas
RUN pip install numpy

CMD [ "python", "./ComputeMetrics.py" ]
