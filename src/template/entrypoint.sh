#!/bin/bash

while ! nc -z postgres 5432; do sleep 1; done;
