# frontend build stage
FROM node:lts as frontend-build-stage
WORKDIR /front
COPY frontend/ .
RUN npm install && npm run build


# production stage
FROM nginx/unit:1.26.1-python3.10

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install -U python-dotenv

COPY /backend /backend
COPY backend/.env .env
COPY --from=frontend-build-stage /front/dist /frontend

COPY nginx/config.json /docker-entrypoint.d/config.json
COPY nginx/bundle.pem /docker-entrypoint.d/bundle.pem