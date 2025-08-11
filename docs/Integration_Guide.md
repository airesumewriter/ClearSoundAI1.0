# Integration Guide - AI Model Module

This guide explains how to integrate the AI Model Integration Module into the ClearSound AI main repo.

Steps:
1. Place this module under /modules/ai_model in the monorepo.
2. Ensure Python environment has dependencies from requirements.txt
3. Expose REST API via reverse proxy (e.g., /api/v1/model -> module's /process)
4. Configure Dockerfile and service in docker-compose or k8s
5. Update main /docs/patent-log.md with any novel additions (see note_on_ip.md)
