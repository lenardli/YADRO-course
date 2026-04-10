FROM python:3.13-slim-trixie@sha256:739e7213785e88c0f702dcdc12c0973afcbd606dbf021a589cab77d6b00b579d AS build

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --prefix=/install -r requirements.txt

COPY . .


FROM gcr.io/distroless/python3-debian13:nonroot@sha256:cb8e12bde699c3912ed13022ed9aba6a9e6f093cf6e3ad5ded0fca36ccaedf93 AS prod

WORKDIR /app
USER 65532:65532

ENV PYTHONPATH=/site-packages \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

COPY --from=build --chown=65532:65532 /install/lib/python3.13/site-packages /site-packages
COPY --from=build --chown=65532:65532 /app /app

EXPOSE 8000

CMD ["main.py"]

