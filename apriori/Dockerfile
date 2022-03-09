FROM ubuntu
VOLUME /app
WORKDIR /app
COPY . .
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y \
   python3-pip
RUN apt-get install -y wget
RUN pip3 install streamlit
EXPOSE 8501
ENTRYPOINT streamlit run apriori_main.py