FROM python:3


#prepare python environment
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

#prepare app

COPY library ./library
COPY picentral.py ./

CMD [ "python", "picentral.py"]
