FROM akraradets/ait-ml-base:2023

RUN pip3 install --upgrade pip
RUN pip3 install ipykernel
RUN pip3 install scikit-learn==1.3.2
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install mlflow

CMD tail -f /dev/null