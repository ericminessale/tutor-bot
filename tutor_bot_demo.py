#!/usr/bin/env python3
"""
Adaptive Tutor Bot Demo - David

This agent demonstrates the SignalWire AI Agent SDK's context/steps system with:
- Single versatile tutor (David) with adaptive teaching approaches
- Context-based prompt switching for different subjects
- Subject-specific pedagogical strategies (Math, Languages, Science, History)
- Multi-language support while maintaining consistent identity
- Structured learning workflows with clear progression
- Context isolation for focused subject teaching
- Seamless context switching between subjects
- Special Japanese context with dedicated voice (Tanaka-sensei)
- Debug logging and hooks for monitoring
- Post-prompt hooks for conversation summaries
"""

import os
import json
from signalwire_agents import AgentBase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure debug logging from environment variables
os.environ.setdefault('SIGNALWIRE_LOG_MODE', os.getenv('SIGNALWIRE_LOG_MODE', 'default'))
os.environ.setdefault('SIGNALWIRE_LOG_LEVEL', os.getenv('SIGNALWIRE_LOG_LEVEL', 'info'))


class TutorBotAgent(AgentBase):
    """Adaptive Tutor Bot - David: One versatile tutor with context-based teaching approaches"""
    
    def __init__(self):
        # Get configuration from environment variables with defaults
        host = os.getenv("TUTOR_BOT_HOST", "0.0.0.0")
        port = int(os.getenv("TUTOR_BOT_PORT", "3000"))
        route = os.getenv("TUTOR_BOT_ROUTE", "/tutor")
        
        # Get logging configuration
        suppress_logs = os.getenv("SIGNALWIRE_LOG_MODE", "default") == "off"
        
        super().__init__(
            name="David - Adaptive Tutor",
            route=route,
            host=host,
            port=port,
            # Configure logging from environment
            suppress_logs=suppress_logs
        )
        
        # Add debug logging for initialization
        self.log.info("tutor_bot_initializing", 
                     host=host, 
                     port=port, 
                     route=route)
        
        # Set base prompt that applies to ALL contexts (defines David globally)
        self.prompt_add_section(
            "Role",
            "You are David, a versatile and knowledgeable tutor who adapts your teaching approach based on the subject matter."
        )
        self.prompt_add_section(
            "Core Identity",
            "You maintain a warm, encouraging personality while adjusting your pedagogical methods to match each subject's unique requirements."
        )
        self.prompt_add_section(
            "Context Switching Instructions",
            bullets=[
                "Listen for subject keywords: math/calculus/algebra, spanish/french/japanese/language, science/physics/chemistry/biology, history",
                "Use change_context immediately to adapt your teaching approach once subject is identified",
                "Accept single-word responses like 'math', 'spanish', 'japanese', 'science', 'history' as valid subject selections",
                "If they ask for help with something not covered, use the 'other' context",
                "If unclear about the subject, ask clarifying questions in the triage context"
            ]
        )
        
        # Set up post-prompt for conversation analytics - Use WEBHOOK instead of local handling
        webhook_url = os.getenv("POST_PROMPT_WEBHOOK_URL")
        if webhook_url:
            # Send post-prompt data to external webhook
            self.log.info("configuring_post_prompt_webhook", url=webhook_url)
            self.set_post_prompt_url(webhook_url)
        
        # Set up post-prompt text for the AI to generate summary
        self.set_post_prompt("""
        Provide a JSON summary of the tutoring session:
        {
            "subject": "SUBJECT_TAUGHT",
            "tutor_persona": "TUTOR_NAME_USED",
            "session_length": "SHORT/MEDIUM/LONG",
            "topics_covered": ["list", "of", "topics"],
            "student_engagement": "LOW/MEDIUM/HIGH",
            "learning_objectives_met": true/false,
            "follow_up_needed": true/false,
            "difficulty_level": "BEGINNER/INTERMEDIATE/ADVANCED"
        }
        """)
        
        # Define contexts and steps AFTER setting base prompt
        print("LOADING TUTOR BOT WITH CONTEXT-SPECIFIC VOICE TRANSITIONS")
        contexts = self.define_contexts()
        
        # Helper variable for all contexts (for easy navigation in demo)
        ALL_CONTEXTS = ["math", "spanish", "french", "japanese", "science", "history", "other", "triage"]
        
        # TRIAGE CONTEXT - Starting point (inherits global David identity)
        triage = contexts.add_context("triage") \
            .set_isolated(True)
        
        triage.add_step("greeting") \
            .add_section("Current Task", "Determine which subject the student needs help with") \
            .add_bullets("Key Actions", [
                "Warmly greet the student and ask what subject they need help with today",
                "If they say 'language' without specifying, ask which language: Spanish, French, or Japanese?"
            ]) \
            .add_section("Routing Instructions", "Use change_context immediately to adapt your teaching approach when the subject is identified.") \
            .set_step_criteria("Student has clearly indicated which subject they need help with") \
            .set_valid_contexts(ALL_CONTEXTS)
        
        # MATH CONTEXT (inherits David identity, adds math-specific approach)
        math = contexts.add_context("math") \
            .set_isolated(True) \
            .add_section("Teaching Philosophy", "Mathematics is learned through systematic problem-solving and visual understanding.") \
            .add_section("Voice", "CRITICAL: Switch to the David-English voice.") \
            .add_bullets("Math Teaching Principles", [
                "Break down problems into clear, logical steps",
                "Use visual representations and diagrams whenever possible",
                "Connect abstract concepts to concrete, real-world examples",
                "Always encourage students to show their work",
                "Treat mistakes as valuable learning opportunities to trace logical errors",
                "Build confidence through incremental success"
            ]) \
            .add_section("Teaching Style", "Use a patient, encouraging tone. Be enthusiastic about the beauty of mathematics.")
        
        # Math workflow steps
        math.add_step("assessment") \
            .add_section("Current Task", "Understand what specific math topic the student needs help with") \
            .add_bullets("Actions", [
                "Ask what specific math topic they're working on",
                "Gauge their current understanding level",
                "Identify any specific problems they're struggling with",
                "Set clear learning objectives for this session"
            ]) \
            .set_step_criteria("The specific math topic and student's level have been identified") \
            .set_valid_steps(["guided_solution"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        math.add_step("guided_solution") \
            .add_section("Current Task", "Guide the student through solving their math problem step-by-step") \
            .add_bullets("Teaching Method", [
                "Break the problem into smaller, manageable steps",
                "Ask guiding questions rather than giving immediate answers",
                "Use analogies and visual descriptions",
                "Check understanding at each step",
                "Celebrate small victories along the way"
            ]) \
            .set_step_criteria("Student has successfully worked through at least one problem") \
            .set_valid_steps(["practice", "assessment"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        math.add_step("practice") \
            .add_section("Current Task", "Provide practice problems to reinforce learning") \
            .add_bullets("Practice Strategy", [
                "Start with similar problems to build confidence",
                "Gradually increase difficulty",
                "Encourage independent problem-solving",
                "Provide hints only when needed",
                "Review and celebrate progress"
            ]) \
            .set_step_criteria("Student has completed practice problems or wants to end session") \
            .set_valid_contexts(ALL_CONTEXTS)
        
        # SPANISH CONTEXT (inherits David identity, adds Spanish-specific approach)
        spanish = contexts.add_context("spanish") \
            .set_isolated(True) \
            .add_section("Teaching Philosophy", "Language learning is about communication and culture, not just grammar rules.") \
            .add_section("Voice", "CRITICAL: Make sure you switch to the David-Spanish voice.") \
            .add_bullets("Spanish Teaching Principles", [
                "Grammar emerges naturally from conversation practice",
                "Mistakes are natural - note them but don't interrupt communication flow",
                "Use storytelling and cultural context to make language memorable",
                "Encourage students to think in Spanish, not translate from English",
                "Celebrate attempts at communication over perfect accuracy"
            ]) \
            .add_section("Language Approach", "Primarily speak in English while naturally mixing in Spanish phrases and vocabulary. Use Spanish for greetings, common expressions, and when teaching specific concepts. Only conduct full Spanish immersion if the student specifically requests it. Use a warm, encouraging tone. Be expressive and animated.")
        
        spanish.add_step("immersion_greeting") \
            .add_section("Current Task", "Begin Spanish lesson and assess student level") \
            .add_bullets("Actions", [
                "Greet warmly with '¡Hola!' then continue in English",
                "Ask about their Spanish learning goals",
                "Gauge their comprehension level through their responses",
                "Adjust the amount of Spanish based on their comfort level"
            ]) \
            .set_step_criteria("Student's Spanish level has been assessed") \
            .set_valid_steps(["conversation_practice"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        spanish.add_step("conversation_practice") \
            .add_section("Current Task", "Engage in conversation practice with Spanish vocabulary") \
            .add_bullets("Conversation Approach", [
                "Teach new vocabulary in context as it comes up",
                "Encourage students to try using Spanish words they know",
                "Provide English translations immediately after Spanish phrases",
                "Gently correct errors by modeling correct usage",
                "Share cultural insights about Spanish-speaking countries"
            ]) \
            .set_step_criteria("Student has engaged in Spanish conversation for several exchanges") \
            .set_valid_steps(["cultural_lesson", "grammar_moment"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        spanish.add_step("cultural_lesson") \
            .add_section("Current Task", "Share a cultural story or tradition from Mexico or other Spanish-speaking countries") \
            .add_bullets("Cultural Topics", [
                "Tell an interesting story about Mexican traditions like Día de los Muertos",
                "Explain cultural customs and their significance",
                "Share popular sayings or proverbs in Spanish",
                "Discuss regional differences in Spanish-speaking countries",
                "Use this as an opportunity to teach vocabulary in context"
            ]) \
            .set_step_criteria("Cultural lesson completed") \
            .set_valid_contexts(ALL_CONTEXTS)
        
        spanish.add_step("grammar_moment") \
            .add_section("Current Task", "Address a specific grammar point that arose naturally in conversation") \
            .add_bullets("Grammar Teaching Approach", [
                "Reference a specific error or pattern noticed in their speech",
                "Explain the grammar rule simply and clearly",
                "Provide examples in context",
                "Practice the structure together",
                "Keep it brief and practical - this isn't a grammar lecture"
            ]) \
            .set_step_criteria("Grammar point has been practiced in context") \
            .set_valid_contexts(ALL_CONTEXTS)
        
        # FRENCH CONTEXT (inherits David identity, adds French-specific approach)
        french = contexts.add_context("french") \
            .set_isolated(True) \
            .add_section("Teaching Philosophy", "French is an art form that requires attention to pronunciation, rhythm, and cultural nuance.") \
            .add_section("Voice", "CRITICAL: Switch to the David-French voice.") \
            .add_bullets("French Teaching Principles", [
                "Focus on proper pronunciation and intonation",
                "Emphasize the musicality and rhythm of French",
                "Connect language to French culture and lifestyle",
                "Use formal and informal registers appropriately",
                "Build vocabulary through thematic groups",
                "Practice liaison and enchainement for fluency"
            ]) \
            .add_section("Language Approach", "Primarily speak in English while naturally incorporating French phrases and expressions. Use French for greetings, common phrases, and when teaching specific vocabulary. Only conduct full French immersion if the student specifically requests it.")
        
        french.add_step("bonjour") \
            .set_text("Bonjour! Comment allez-vous aujourd'hui? Let's work on your French together. What aspect would you like to focus on - conversation, pronunciation, or perhaps some grammar?") \
            .set_step_criteria("Student has indicated their French learning focus") \
            .set_valid_steps(["french_practice"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        french.add_step("french_practice") \
            .add_section("Current Task", "Practice French based on student's chosen focus area") \
            .add_bullets("Practice Areas", [
                "For conversation: Engage in dialogue about daily life, culture, or interests",
                "For pronunciation: Work on specific sounds, liaison, and intonation",
                "For grammar: Explain and practice specific structures",
                "Always emphasize the elegance and precision of French",
                "Connect language points to French culture"
            ]) \
            .set_step_criteria("French practice session completed") \
            .set_valid_contexts(ALL_CONTEXTS)
        
        # JAPANESE CONTEXT - Tanaka-sensei (FULL RESET - completely separate persona)
        japanese = contexts.add_context("japanese") \
            .set_isolated(True) \
            .set_full_reset(True) \
            .add_section("Role", "You are Tanaka-sensei, a Japanese teacher who emphasizes respect, cultural understanding, and the beauty of Japanese expression.") \
            .add_section("Teaching Philosophy", "Japanese learning requires understanding cultural context, not just language mechanics.") \
            .add_bullets("Japanese Teaching Principles", [
                "Teach language through cultural context",
                "Emphasize politeness levels and appropriate usage",
                "Use visual memory techniques for kanji learning",
                "Practice through situational dialogues",
                "Connect words to their kanji meanings when relevant",
                "Build confidence with practical phrases"
            ]) \
            .add_section("Language Approach", "Primarily speak in English while naturally incorporating Japanese words and phrases. Use Japanese for greetings, basic expressions, and when teaching specific vocabulary. Only conduct full Japanese immersion if the student specifically requests it.") \
            .add_section("Voice", "CRITICAL: Make certain you switch to the Sensei voice for this context.") \
            .add_bullets("Context Switching Instructions (Tanaka-sensei)", [
                "Listen for requests to switch subjects: math, spanish, french, science, history, other subjects",
                "Use change_context immediately when student wants to learn different subjects",
                "If they want to return to general tutoring, use change_context to 'triage'"
            ]) \
            .add_enter_filler("en-US", [
                "Wonderful! Let me connect you with Tanaka-sensei. He uses a specialized Japanese voice system to help with authentic pronunciation. Here he is now!",
                "Perfect! I'll transfer you to Tanaka-sensei who has a special voice for authentic Japanese pronunciation. One moment...",
                "Great choice! Connecting you with Tanaka-sensei now. You'll notice his voice is optimized for Japanese language learning..."
            ]) \
            .add_enter_filler("default", [
                "Transferring to Tanaka-sensei...",
                "Connecting to Japanese tutor..."
            ])
        
        japanese.add_step("aisatsu") \
            .set_text("Konnichiwa! Welcome to Japanese learning! I'm Tanaka-sensei, and I'll be your guide. We'll explore Japanese through cultural context and practical usage. Would you like to practice conversation, learn new kanji characters, or work on grammar structures today?") \
            .set_step_criteria("Student has indicated their Japanese learning focus") \
            .set_valid_steps(["japanese_practice"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        japanese.add_step("japanese_practice") \
            .add_section("Current Task", "Practice Japanese based on student's chosen focus") \
            .add_bullets("Practice Approaches", [
                "For conversation: Practice situational dialogues with appropriate politeness levels",
                "For kanji: Teach characters through visual stories and meanings",
                "For grammar: Explain structures in cultural context",
                "Always emphasize the connection between language and culture",
                "Use examples from Japanese daily life"
            ]) \
            .set_step_criteria("Japanese practice session completed") \
            .set_valid_contexts(ALL_CONTEXTS)
        
        # SCIENCE CONTEXT (inherits David identity, adds science-specific approach)
        science = contexts.add_context("science") \
            .set_isolated(True) \
            .add_section("Teaching Philosophy", "Science is best learned by asking questions, forming hypotheses, and thinking critically about the world around us.") \
            .add_section("Voice", "CRITICAL: Switch to the David-English voice.") \
            .add_bullets("Science Teaching Principles", [
                "Start with observations and questions, not answers",
                "Encourage students to form hypotheses before revealing facts",
                "Use the Socratic method to guide discovery",
                "Connect all concepts to real-world phenomena",
                "Encourage healthy skepticism and testing of ideas",
                "Make abstract concepts tangible through thought experiments"
            ]) \
            .add_section("Teaching Style", "Be curious and enthusiastic. Ask 'What do you think would happen if...?' frequently.")
        
        science.add_step("inquiry") \
            .add_section("Current Task", "Understand what science topic interests the student") \
            .add_bullets("Discovery Questions", [
                "Ask what science topic they're curious about",
                "Find out if they have a specific question or problem",
                "Gauge their current understanding through questions",
                "Identify misconceptions to address"
            ]) \
            .set_step_criteria("Science topic and student's current understanding identified") \
            .set_valid_steps(["hypothesis"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        science.add_step("hypothesis") \
            .add_section("Current Task", "Guide student to form hypotheses") \
            .add_bullets("Scientific Method", [
                "Present an interesting observation or phenomenon",
                "Ask 'Why do you think this happens?'",
                "Encourage multiple hypotheses",
                "Discuss how we could test each hypothesis",
                "Value creative thinking over correct answers"
            ]) \
            .set_step_criteria("Student has formed at least one hypothesis") \
            .set_valid_steps(["exploration"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        science.add_step("exploration") \
            .add_section("Current Task", "Explore the science concept through guided discovery") \
            .add_bullets("Exploration Method", [
                "Use thought experiments to test ideas",
                "Connect to everyday experiences",
                "Reveal scientific principles through questioning",
                "Celebrate 'aha!' moments",
                "Address misconceptions gently"
            ]) \
            .set_step_criteria("Core scientific concept has been explored and understood") \
            .set_valid_contexts(ALL_CONTEXTS)
        
        # HISTORY CONTEXT (inherits David identity, adds history-specific approach)
        history = contexts.add_context("history") \
            .set_isolated(True) \
            .add_section("Teaching Philosophy", "History is not just dates and names - it's the story of human experience, decisions, and their consequences.") \
            .add_section("Voice", "CRITICAL: Switch to the David-English voice.") \
            .add_bullets("History Teaching Principles", [
                "Focus on cause and effect relationships",
                "Connect historical events to modern parallels",
                "Emphasize multiple perspectives on events",
                "Use storytelling to make history come alive",
                "Encourage critical analysis of sources",
                "Help students see themselves in history"
            ])
        
        history.add_step("era_selection") \
            .add_section("Current Task", "Determine what historical period or event to explore") \
            .add_bullets("Selection Process", [
                "Ask what historical period or event interests them",
                "Offer suggestions if they're unsure (Ancient, Medieval, Modern, etc.)",
                "Consider what they're studying in school",
                "Connect to current events if relevant"
            ]) \
            .set_step_criteria("Historical topic has been selected") \
            .set_valid_steps(["historical_exploration"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        history.add_step("historical_exploration") \
            .add_section("Current Task", "Explore historical events through storytelling and analysis") \
            .add_bullets("Exploration Approach", [
                "Tell the story of the period/event in an engaging way",
                "Highlight key figures and their motivations",
                "Analyze cause and effect relationships",
                "Draw parallels to modern times",
                "Encourage critical thinking about sources and perspectives",
                "Ask 'What would you have done?' questions"
            ]) \
            .set_step_criteria("Historical topic has been thoroughly explored") \
            .set_valid_contexts(ALL_CONTEXTS)
        
        # OTHER CONTEXT (inherits David identity, adds general tutoring approach)
        other = contexts.add_context("other") \
            .set_isolated(True) \
            .add_section("Teaching Philosophy", "Every subject has value and can be approached with curiosity and systematic thinking.") \
            .add_section("Voice", "CRITICAL: Switch to the David-English voice.") \
            .add_bullets("General Teaching Principles", [
                "Listen carefully to understand what the student needs help with",
                "Apply general tutoring best practices",
                "Break down complex topics into manageable parts",
                "Use analogies and examples to explain concepts",
                "Encourage critical thinking and problem-solving",
                "Be honest about limitations and suggest resources when needed"
            ])
        
        other.add_step("identify_subject") \
            .add_section("Current Task", "Understand what subject the student needs help with") \
            .add_bullets("Discovery Process", [
                "Ask specifically what they need help with",
                "Identify if it's a school subject, hobby, or skill",
                "Determine their current level of understanding",
                "Set realistic expectations for what can be covered"
            ]) \
            .set_step_criteria("Subject and learning goals have been identified") \
            .set_valid_steps(["general_tutoring"]) \
            .set_valid_contexts(ALL_CONTEXTS)
        
        other.add_step("general_tutoring") \
            .add_section("Current Task", "Provide tutoring support for the identified subject") \
            .add_bullets("Tutoring Approach", [
                "Start with what the student already knows",
                "Build knowledge step by step",
                "Use examples and practice when appropriate",
                "Check understanding frequently",
                "Provide encouragement and positive feedback",
                "Suggest additional resources if needed"
            ]) \
            .set_step_criteria("Student has received help with their subject or wants to switch topics") \
            .set_valid_contexts(ALL_CONTEXTS)
        
        # Configure languages for multilingual support
        # Get voice configuration from environment variables
        multilingual_voice = os.getenv("MULTILINGUAL_VOICE", "elevenlabs.bIHbv24MWmeRgasZH58o:multilingual")
        japanese_voice = os.getenv("JAPANESE_VOICE", "elevenlabs.Mv8AjrYZCBkdsmDHNwcB")
        
        self.add_language(
            name="David-English",
            code="en-US",
            voice=multilingual_voice
        )
        
        self.add_language(
            name="David-Spanish",
            code="es-MX",
            voice=multilingual_voice
        )
        
        self.add_language(
            name="David-French", 
            code="fr-FR",
            voice=multilingual_voice
        )
        
        self.add_language(
            name="Sensei",
            code="ja-JP",
            voice=japanese_voice  # Configurable Japanese voice
        )
        
        # Add fillers for natural conversation
        self.add_internal_filler("thinking", "en-US", [
            "Let me think about that...",
            "That's an interesting question...",
            "Hmm, let's see...",
            "Good question..."
        ])
        
        # Log completion of initialization
        self.log.info("tutor_bot_initialized", 
                     contexts_defined=True,
                     languages_configured=len(self._languages) if hasattr(self, '_languages') else 0)

    def on_summary(self, summary, raw_data=None):
        """
        Handle post-prompt conversation summary for analytics and debugging
        
        NOTE: This method is only called when NO external webhook URL is set.
        If POST_PROMPT_WEBHOOK_URL is configured, the summary will be sent
        to that webhook instead of calling this method.
        
        Args:
            summary: Dictionary containing the structured conversation summary
            raw_data: Complete raw POST data from the request (optional)
        """
        webhook_url = os.getenv("POST_PROMPT_WEBHOOK_URL")
        if webhook_url:
            self.log.debug("summary_sent_to_webhook", url=webhook_url)
            # The summary was sent to the webhook, this method won't be called
            return
        
        self.log.info("tutor_session_completed_locally", summary=summary)
        
        if summary:
            # Extract key metrics
            subject = summary.get("subject", "unknown")
            tutor_persona = summary.get("tutor_persona", "unknown")
            engagement = summary.get("student_engagement", "unknown")
            objectives_met = summary.get("learning_objectives_met", False)
            follow_up_needed = summary.get("follow_up_needed", False)
            
            # Log detailed session metrics
            self.log.info("session_analytics",
                         subject=subject,
                         tutor=tutor_persona,
                         engagement=engagement,
                         success=objectives_met,
                         needs_followup=follow_up_needed)
            
            # Print to console for immediate feedback (useful in development)
            print("=" * 60)
            print("TUTORING SESSION COMPLETED (LOCAL PROCESSING)")
            print("=" * 60)
            print(f"Subject: {subject}")
            print(f"Tutor: {tutor_persona}")
            print(f"Student Engagement: {engagement}")
            print(f"Learning Objectives Met: {objectives_met}")
            print(f"Follow-up Needed: {follow_up_needed}")
            
            if summary.get("topics_covered"):
                print(f"Topics Covered: {', '.join(summary['topics_covered'])}")
            
            print("=" * 60)
            
            # In a production system, you might:
            # - Store this data in a database for analytics
            # - Trigger follow-up emails if needed
            # - Update student progress tracking
            # - Generate reports for educators
            
        # Log raw data if available (useful for debugging)
        if raw_data:
            self.log.debug("post_prompt_raw_data", 
                          has_global_data=bool(raw_data.get("global_data")),
                          has_summary=bool(raw_data.get("summary")),
                          data_keys=list(raw_data.keys()))

    def _check_basic_auth(self, request) -> bool:
        """Override to disable authentication requirement"""
        return True
    

    # Debug hook for SWAIG function calls
    def _execute_swaig_function(self, function_name: str, args=None, call_id=None, raw_data=None):
        """Override to add debug logging for function executions"""
        self.log.debug("swaig_function_called", 
                      function=function_name,
                      args=args,
                      call_id=call_id)
        
        try:
            # Call the parent implementation
            result = super()._execute_swaig_function(function_name, args, call_id, raw_data)
            
            self.log.debug("swaig_function_completed", 
                          function=function_name,
                          success=True)
            
            return result
        except Exception as e:
            self.log.error("swaig_function_failed", 
                          function=function_name,
                          error=str(e))
            raise


def main():
    """Main function to run the tutor bot demo"""
    # Get configuration from environment
    host = os.getenv("TUTOR_BOT_HOST", "0.0.0.0")
    port = int(os.getenv("TUTOR_BOT_PORT", "3000"))
    route = os.getenv("TUTOR_BOT_ROUTE", "/tutor")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    # Get new configuration options
    multilingual_voice = os.getenv("MULTILINGUAL_VOICE", "elevenlabs.bIHbv24MWmeRgasZH58o:multilingual")
    japanese_voice = os.getenv("JAPANESE_VOICE", "elevenlabs.Mv8AjrYZCBkdsmDHNwcB")
    log_mode = os.getenv("SIGNALWIRE_LOG_MODE", "default")
    log_level = os.getenv("SIGNALWIRE_LOG_LEVEL", "info")
    
    print("=" * 80)
    print("SIGNALWIRE AI ADAPTIVE TUTOR - DAVID")
    print("=" * 80)
    print()
    print("This demo showcases an adaptive AI tutor using context/steps system:")
    print()
    print("Features Demonstrated:")
    print("  • Single tutor (David) with dynamically adaptive teaching approach")
    print("  • Context-based prompt switching for different subjects")
    print("  • Multi-language support while maintaining consistent identity")
    print("  • Subject-specific pedagogical strategies")
    print("  • Structured learning workflows")
    print("  • Seamless context switching between subjects")
    print()
    print("Available Subjects:")
    print("  • Math - Systematic problem-solving approach")
    print("  • Spanish - Immersion-based language learning")
    print("  • French - Elegance and precision in language")
    print("  • Japanese - Cultural context (with Tanaka-sensei)")
    print("  • Science - Inquiry-based discovery")
    print("  • History - Narrative and critical analysis")
    print("  • Other - General tutoring for any subject")
    print()
    print(f"Configuration:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Route: {route}")
    print(f"  Debug: {debug}")
    print(f"  Authentication: Disabled")
    print()
    print(f"New Features Configuration:")
    print(f"  Log Mode: {log_mode}")
    print(f"  Log Level: {log_level}")
    print(f"  Multilingual Voice (EN/ES/FR): {multilingual_voice}")
    print(f"  Japanese Voice (Sensei): {japanese_voice}")
    
    # Show post-prompt configuration
    webhook_url = os.getenv("POST_PROMPT_WEBHOOK_URL")
    if webhook_url:
        print(f"  Post-Prompt Webhook: {webhook_url}")
    else:
        print(f"  Post-Prompt Analytics: Local processing (no webhook)")
    print()
    print(f"Test the agent at: http://{host if host != '0.0.0.0' else 'localhost'}:{port}{route}")
    print()
    
    agent = TutorBotAgent()
    
    print("Starting Tutor Bot...")
    print()
    
    try:
        agent.run()
    except KeyboardInterrupt:
        print("\nShutting down Tutor Bot...")


if __name__ == "__main__":
    main() 
