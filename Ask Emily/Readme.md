# Ask Emily – AI Trip Planner, Travel Advisor, GPS & RV Technician Finder

## Project Overview
This project aims to develop **Ask Emily**, an AI-powered travel assistant that provides tailored trip planning, GPS navigation, and RV-safe route recommendations. Designed with user convenience and accessibility in mind, Ask Emily will feature a chatbot interface for desktop, iOS, and Android platforms, allowing users to interactively explore travel routes, plan trips, and find RV technicians as needed. The assistant will leverage open-source models, maps, and free APIs to offer a comprehensive travel advisory experience.

## Project Objectives
- **Interactive Travel Planning**: Suggests personalized itineraries with day-wise route details and points of interest based on user preferences.
- **RV-Safe Route Suggestions**: Provides route recommendations optimized for RV specifications (size, dimensions, etc.), leveraging height, width, and clearance data for bridges and roads.
- **Dynamic Maps**: Features a real-time, interactive map interface that displays route suggestions and allows users to navigate through day-by-day itineraries with ease.
- **Selectable Suggestions**: Offers users selectable recommendations within the chat, enhancing usability and interaction.

## Development Plan
1. **Phase 1: Chatbot Core**
   - **Objective**: Develop a robust conversational AI assistant using an open-source model.
   - **Approach**: Fine-tune the assistant on travel-specific data, with a focus on RV-friendly routes, integrating prompts to cater to both general travelers and RV-specific needs.

2. **Phase 2: Data Collection and Route Optimization**
   - **Objective**: Collect and incorporate data on RV dimensions, bridge heights, and road widths to enhance route suitability.
   - **Approach**: Integrate data from free sources and APIs to ensure safety and comfort for RV travelers, with particular attention to bridge clearances and road widths.

3. **Phase 3: Web-Based Interface with Map Integration**
   - **Objective**: Create a user-friendly web-based interface where chat and map windows co-exist.
   - **Features**: 
     - Split-screen design with a chat box and interactive map view.
     - A dynamic display of routes and map markers based on user inputs and day-by-day itinerary.
     - Next and Previous buttons for multi-day route navigation.
     - Interactive, selectable suggestions within the chat interface for streamlined user experience.

4. **Phase 4: User Experience & Value Enhancement**
   - **Objective**: Enhance the chatbot’s response quality and the UI’s intuitiveness.
   - **Scope for Improvement**:
     - Explore additional integrations, such as tapping/clicking on chatbot suggestions.
     - Leverage analytics to understand user preferences better and iterate on commonly requested features.
     - Develop an intuitive, visually engaging UI that fosters high user engagement.

## Business Value
This application is designed to offer value to travelers, specifically RV enthusiasts, by providing safe, optimized routes and route-specific guidance. In addition to providing a convenient tool for planning trips, **Ask Emily** has potential for monetization through premium features, advertising partnerships, or affiliate links for campgrounds, equipment, or travel insurance, creating a new revenue channel for the company.

## Current Progress

1. **Chatbot Development**  
   - Set up a conversational AI assistant prototype on Google Colab, using open-source language models to generate preliminary travel recommendations. Initial model responses were tested and iterated upon to refine conversational quality and route suggestions.
   
2. **Web-Based Interface Skeleton**  
   - Developed an initial web-based chat interface framework in Colab, featuring a split layout that displays chat responses alongside dynamically generated maps.
   - Organized project files for integration with the main interface, focusing on seamless expansion as new functionalities are developed.

All prototype code, experimental files, and additional resources are provided in this repository.

## Future Scope
The next steps involve completing the integration of RV-specific data, refining map functionality, and enhancing the user interface to improve overall experience and interaction. These improvements will ensure Ask Emily is positioned as a unique, value-driven travel assistant for a wide user base.
