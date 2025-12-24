# Pictovector - React + Flask + Qdrant

This fun little project was developed for one of the LabLab.ai's hackathon.

[!IMPORTANT]
Vercel's free tier requires the build file to be at max 250 MB but since we
use local models (Huggingface, pytorch) the file goes beyond the limit.
In order to work in vercel, you need paid tier.

## What is Pictovector?

**Pictovector** is an image repository with vector search; powered by
Qdrant. 

## Who is it for and why?

The project aims to solve the challenges faced by photographers, artists and
people who have a huge archive of images

### Challenges Pictovector tries to solve -
* Accessing images that are hidden in a huge archive
* Manual tagging of the images; Error prone and thousands of possible tags
* Limited search capabilities using only metadata and filenames.
* Clustering similar themed images

## How?

When managing an archive of several hundred thousand or even millions of images, traditional metadata and tag-based
searches often fail. In the AI era, relying on tags you might have forgotten or filenames you never properly assigned
should be a last resort. Instead of struggling to remember specific labels, you can now search based on the visual
memory of your work.

Pictovector leverages semantic and similarity search to bridge the gap between your memory and your digital archive.
By using vector embeddings, the system understands the actual content of your images, allowing you to bypass rigid
folder structures and manual organization.

### Key Features of Pictovector:
* **Neural Vector Embeddings:** Deeply understands the visual context and "essence" of every image or sketch.


* **Automated Tagging:** Generates intelligent, descriptive tags for granular filtering without manual effort.


* **AI-Powered Captioning:** Automatically produces detailed descriptions and captions for every file in your library.


* **Natural Language Search:** Find exactly what you are looking for by describing it in plain English—no keywords required.

## Tech Stack:

### Frontend:
Javascript, React, Vite

### Backend:
Python, Flask, HuggingFace, GeminiAPI, Qdrant, Hatch

### Models & Embeddings:
* Models - 

  1. Gemini-2.5-flash (Gemini API) - Tag and description generation
  2. Google embeddings (Gemini API) - Text embeddings
  3. Microsoft/resnet-50 (HuggingFace) - Image embeddings

[!NOTE]
We could've avoided two embeddings using multimodal models like
OpenAI's Clip but as this is an hackathon project we had to use gemini api
and it was fun implementing a different approach.

### Serve:
Vercel

[!NOTE]
Vercel is not linked to this repository.

## Developed by:

* **Frontend** - [Uroj Ashfa](https://github.com/UroojAshfa)
* **Backend** - [Ilamaran Magesh](https://github.com/IlamaranMagesh)