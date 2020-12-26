FROM python:3


#prepare python environment
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

#prepare app
COPY ib ./xml
COPY library ./library
COPY picentral.py ./

CMD [ "python", "picentral.py"]
# ["ls", "/usr/src/app"]

#run with: docker run -d -p 5000:5000 -t picentral