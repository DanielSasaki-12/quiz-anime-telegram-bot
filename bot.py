import os
import json
import random
import time
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Configuration des logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token depuis les variables d'environnement (sécurisé)
BOT_TOKEN = os.getenv('BOT_TOKEN', '8458879508:AAGavGjA2qn-RUcSaaHLAM96--lS0yzNqG8')

# Questions du quiz ULTRA COMPLET - 15 questions par partie
QUESTIONS = [
    # === QUESTIONS FACILES (Niveau Apprenti) ===
    {
        # Créer le texte de la question avec indicateurs visuels selon la difficulté
        difficulty_emoji = {
            "easy": "🟢", 
            "medium": "🟡", 
            "hard": "🔴", 
            "nightmare": "💜",
            "impossible": "🖤"
        }
        difficulty_names = {
            "easy": "Facile",
            "medium": "Moyen", 
            "hard": "Difficile", 
            "nightmare": "Cauchemar",
            "impossible": "Impossible"
        }"type": "text",
        "question": "Quel est le nom du personnage principal de Naruto ?",
        "options": ["Naruto Uzumaki", "Sasuke Uchiha", "Sakura Haruno", "Kakashi Hatake"],
        "correct": 0,
        "difficulty": "easy",
        "anime": "Naruto"
    },
    {
        "type": "image",
        "question": "Qui est ce personnage avec son chapeau de paille iconique ?",
        "image_url": "https://static.wikia.nocookie.net/onepiece/images/7/76/Monkey_D._Luffy_Anime_Post_Timeskip.png",
        "options": ["Ace", "Sabo", "Monkey D. Luffy", "Shanks"],
        "correct": 2,
        "difficulty": "easy",
        "anime": "One Piece"
    },
    {
        "type": "audio",
        "question": "De quel anime vient cet opening légendaire ? (We Are!)",
        "audio_url": "https://youtu.be/JX3m5h_f3RM",
        "options": ["Dragon Ball", "One Piece", "Fairy Tail", "Bleach"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "One Piece"
    },
    {
        "type": "text",
        "question": "Quelle est la technique signature de Goku dans Dragon Ball ?",
        "options": ["Rasengan", "Kamehameha", "Chidori", "Bankai"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "Dragon Ball"
    },
    {
        "type": "image",
        "question": "Reconnaissez-vous ce jeune héros aux cicatrices caractéristiques ?",
        "image_url": "https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/7/70/Tanjiro_Kamado.png",
        "options": ["Zenitsu Agatsuma", "Tanjiro Kamado", "Inosuke Hashibira", "Giyu Tomioka"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "Demon Slayer"
    },

    # === QUESTIONS MOYENNES (Niveau Amateur/Fan) ===
    {
        "type": "audio",
        "question": "Quel anime a cet opening épique ? (Guren no Yumiya)",
        "audio_url": "https://youtu.be/XMXgHfHxKVM",
        "options": ["Tokyo Ghoul", "Attack on Titan", "Parasyte", "Kabaneri"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Attack on Titan"
    },
    {
        "type": "image",
        "question": "Qui est ce personnage aux cheveux verts bouclés ?",
        "image_url": "https://static.wikia.nocookie.net/bokunoheroacademia/images/2/29/Izuku_Midoriya.png",
        "options": ["Katsuki Bakugo", "Shoto Todoroki", "Izuku Midoriya", "Tenya Iida"],
        "correct": 2,
        "difficulty": "medium",
        "anime": "My Hero Academia"
    },
    {
        "type": "text",
        "question": "Dans Hunter x Hunter, quelle technique utilise Gon Freecss ?",
        "options": ["Nen", "Jajanken", "Hatsu", "Zetsu"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Hunter x Hunter"
    },
    {
        "type": "audio",
        "question": "De quel anime récent vient cet opening ? (Gurenge)",
        "audio_url": "https://youtu.be/Xy2Q3ZECqfI",
        "options": ["Jujutsu Kaisen", "Demon Slayer", "Chainsaw Man", "Tokyo Revengers"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Demon Slayer"
    },
    {
        "type": "image",
        "question": "Reconnaissez-vous ce Saiyan légendaire ?",
        "image_url": "https://static.wikia.nocookie.net/dragonball/images/6/6d/Goku_anime.png",
        "options": ["Vegeta", "Gohan", "Goku", "Trunks"],
        "correct": 2,
        "difficulty": "medium",
        "anime": "Dragon Ball"
    },

    # === QUESTIONS DIFFICILES (Niveau Expert) ===
    {
        "type": "audio",
        "question": "Quel anime culte a cet opening jazz légendaire ? (Tank!)",
        "audio_url": "https://youtu.be/n2rVnRwW0h8",
        "options": ["Samurai Champloo", "Cowboy Bebop", "Black Lagoon", "Trigun"],
        "correct": 1,
        "difficulty": "hard",
        "anime": "Cowboy Bebop"
    },
    {
        "type": "image",
        "question": "Qui est ce personnage mystérieux avec un carnet de la mort ?",
        "image_url": "https://static.wikia.nocookie.net/deathnote/images/e/e2/Light_Yagami.png",
        "options": ["L Lawliet", "Light Yagami", "Near", "Mello"],
        "correct": 1,
        "difficulty": "hard",
        "anime": "Death Note"
    },
    {
        "type": "text",
        "question": "Dans Steins;Gate, comment s'appelle la machine à voyager dans le temps ?",
        "options": ["Phone Microwave", "Time Leap Machine", "SERN Device", "D-Mail System"],
        "correct": 0,
        "difficulty": "hard",
        "anime": "Steins;Gate"
    },

    # === QUESTIONS TRÈS DIFFICILES (Niveau Cauchemar) ===
    {
        "type": "audio",
        "question": "Quel anime mythique a cet opening ? (A Cruel Angel's Thesis)",
        "audio_url": "https://youtu.be/nU21rCWkuJw",
        "options": ["Serial Experiments Lain", "Neon Genesis Evangelion", "Akira", "Ghost in the Shell"],
        "correct": 1,
        "difficulty": "nightmare",
        "anime": "Neon Genesis Evangelion"
    },
    {
        "type": "image",
        "question": "Qui est ce personnage transformé en ghoul ?",
        "image_url": "https://static.wikia.nocookie.net/tokyoghoul/images/2/24/Kaneki.png",
        "options": ["Touka Kirishima", "Ken Kaneki", "Ayato Kirishima", "Uta"],
        "correct": 1,
        "difficulty": "nightmare",
        "anime": "Tokyo Ghoul"
    },

    # === QUESTIONS IMPOSSIBLES (Niveau Maître Légendaire) ===
    {
        "type": "text",
        "question": "Dans Psycho-Pass, qui contrôle réellement le Sibyl System ?",
        "options": ["Des IA", "Des criminels asympotmatiques", "Le gouvernement", "Des cerveaux de criminels"],
        "correct": 3,
        "difficulty": "impossible",
        "anime": "Psycho-Pass"
    },
    {
        "type": "audio",
        "question": "Quel anime nostalgique a cet opening ? (Butter-Fly)",
        "audio_url": "https://youtu.be/7cSB1IZU_8U",
        "options": ["Pokemon", "Digimon Adventure", "Yu-Gi-Oh!", "Monster Rancher"],
        "correct": 1,
        "difficulty": "impossible",
        "anime": "Digimon Adventure"
    },
    {
        "type": "text",
        "question": "Quel studio a produit 'Your Name' (Kimi no Na wa) ?",
        "options": ["Studio Ghibli", "Madhouse", "CoMix Wave Films", "Toei Animation"],
        "correct": 2,
        "difficulty": "impossible",
        "anime": "Your Name"
    },

    # === QUESTIONS BONUS (Culture Otaku) ===
    {
        "type": "audio",
        "question": "De quel anime moderne vient cet opening ? (Kaikai Kitan)",
        "audio_url": "https://youtu.be/1tk1pqwrOys",
        "options": ["Chainsaw Man", "Jujutsu Kaisen", "Hell's Paradise", "Tokyo Revengers"],
        "correct": 1,
        "difficulty": "hard",
        "anime": "Jujutsu Kaisen"
    },
    {
        "type": "text",
        "question": "Dans quel anime trouve-t-on la technique de respiration 'Hinokami Kagura' ?",
        "options": ["Demon Slayer", "Bleach", "Naruto", "Black Clover"],
        "correct": 0,
        "difficulty": "medium",
        "anime": "Demon Slayer"
    },
    {
        "type": "audio",
        "question": "Quel anime a cet opening énergique ? (Again)",
        "audio_url": "https://youtu.be/2uq34TeWEdQ",
        "options": ["Fullmetal Alchemist", "Fullmetal Alchemist: Brotherhood", "Soul Eater", "D.Gray-man"],
        "correct": 1,
        "difficulty": "hard",
        "anime": "Fullmetal Alchemist: Brotherhood"
    },
    {
        "type": "text",
        "question": "Quel est le nom de l'école dans 'My Hero Academia' ?",
        "options": ["U.A. High School", "Shiketsu High", "Ketsubutsu Academy", "Isamu Academy"],
        "correct": 0,
        "difficulty": "easy",
        "anime": "My Hero Academia"
    },
    {
        "type": "image",
        "question": "Reconnaissez-vous ce personnage principal déterminé ?",
        "image_url": "https://static.wikia.nocookie.net/shingekinokyojin/images/2/26/Eren_Jaeger_Anime.png",
        "options": ["Armin Arlert", "Eren Jaeger", "Levi Ackerman", "Jean Kirstein"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "Attack on Titan"
    },
    {
        "type": "audio",
        "question": "De quel anime classique vient cet opening nostalgique ? (Cha-La Head-Cha-La)",
        "audio_url": "https://youtu.be/Bjf4lB1W0rs",
        "options": ["Dragon Ball", "Dragon Ball Z", "Dragon Ball GT", "Dragon Ball Super"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "Dragon Ball Z"
    },
    {
        "type": "text",
        "question": "Dans Tokyo Revengers, quel est le nom du gang principal de Takemichi ?",
        "options": ["Black Dragons", "Tokyo Manji Gang", "Brahman", "Tenjiku"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Tokyo Revengers"
    },
    {
        "type": "image",
        "question": "Qui est ce personnage blond aux cicatrices sur les joues ?",
        "image_url": "https://static.wikia.nocookie.net/naruto/images/d/d8/Naruto_Part_I.png",
        "options": ["Sasuke Uchiha", "Naruto Uzumaki", "Minato Namikaze", "Boruto Uzumaki"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "Naruto"
    }
]

# Sessions utilisateurs
user_sessions = {}

class AnimeQuizBot:
    def __init__(self, token):
        self.app = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configure les handlers du bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("quiz", self.start_quiz))
        self.app.add_handler(CommandHandler("score", self.show_score))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CallbackQueryHandler(self.handle_answer))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start"""
        welcome_text = """
🎌 **Bienvenue dans le Quiz Anime Universel !** 🎌

Je suis votre bot quiz spécialisé dans l'univers de l'anime !

**🎯 Fonctionnalités :**
- 15 questions par quiz (texte, images, openings)
- Animes du monde entier (classiques & récents)
- Questions chronométrées (10 secondes)
- Difficulté progressive (Facile → Impossible)
- Système de points avec bonus vitesse

**📋 Commandes :**
- /quiz - Commencer un nouveau quiz
- /score - Voir votre score actuel
- /help - Afficher l'aide détaillée

**🏆 Système de points :**
- Bonne réponse : 10 points
- Bonus vitesse : +5 points (< 5 secondes)

Prêt à tester vos connaissances otaku ? Tapez /quiz ! 🚀
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def start_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Démarre un nouveau quiz"""
        user_id = update.effective_user.id
        
        # Sélectionner 15 questions aléatoires pour le quiz complet
        selected_questions = random.sample(QUESTIONS, min(15, len(QUESTIONS)))
        
        user_sessions[user_id] = {
            'questions': selected_questions,
            'current_question': 0,
            'score': 0,
            'start_time': time.time(),
            'question_start_time': time.time()
        }
        
        username = update.effective_user.first_name or "Otaku"
        await update.message.reply_text(
            f"🎯 **Quiz ULTRA démarré pour {username} !**\n\n🌍 15 questions d'animes du monde entier !\n⏰ 10 secondes par question\n🖼️ Images authentiques, 🎵 openings légendaires & 📝 culture otaku !\n🏆 Difficulté progressive jusqu'au niveau impossible !\n\nPremière question arrive...", 
            parse_mode='Markdown'
        )
        await asyncio.sleep(1)
        await self.send_question(update, context, user_id)
    
    async def send_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Envoie une question à l'utilisateur"""
        session = user_sessions.get(user_id)
        if not session:
            return
        
        current_q_index = session['current_question']
        if current_q_index >= len(session['questions']):
            await self.end_quiz(update, context, user_id)
            return
        
        question = session['questions'][current_q_index]
        session['question_start_time'] = time.time()
        
        # Créer le texte de la question
        difficulty_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
        difficulty = question.get('difficulty', 'medium')
        
        question_text = f"**Question {current_q_index + 1}/15** ⏱️\n\n"
        difficulty = question.get('difficulty', 'medium')
        
        question_text += f"🎯 {question['question']}\n\n"
        question_text += f"📚 Anime: {question['anime']}\n"
        question_text += f"💎 Difficulté: {difficulty_emoji[difficulty]} {difficulty_names[difficulty]}\n"
        question_text += f"⏰ Temps: 10 secondes"
        
        # Créer les boutons de réponse
        keyboard = []
        for i, option in enumerate(question['options']):
            keyboard.append([InlineKeyboardButton(f"{chr(65+i)}. {option}", callback_data=f"answer_{i}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Envoyer selon le type de question
        question_type = question.get('type', 'text')
        
        if question_type == 'image' and 'image_url' in question:
            try:
                await context.bot.send_photo(
                    chat_id=user_id,
                    photo=question['image_url'],
                    caption=question_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Erreur envoi image: {e}")
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"🖼️ [Image non disponible]\n\n{question_text}",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        
        elif question_type == 'audio' and 'audio_url' in question:
            try:
                # Pour les openings YouTube, on utilise le lien direct
                if 'youtube.com' in question['audio_url'] or 'youtu.be' in question['audio_url']:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f"🎵 **Opening à identifier :**\n{question['audio_url']}\n\n{question_text}",
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
                else:
                    await context.bot.send_audio(
                        chat_id=user_id,
                        audio=question['audio_url'],
                        caption=question_text,
                        reply_markup=reply_markup,
                        parse_mode='Markdown',
                        title="Opening Anime Quiz",
                        performer="Quiz Anime Bot"
                    )
            except Exception as e:
                logger.error(f"Erreur envoi audio: {e}")
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"🎵 **Opening :** {question['audio_url']}\n\n{question_text}",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        
        else:
            # Question texte normale
            await context.bot.send_message(
                chat_id=user_id,
                text=question_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        # Programmer le timeout à 10 secondes
        context.job_queue.run_once(
            self.question_timeout,
            when=10.0,  # 10 secondes au lieu de 30
            data={'user_id': user_id, 'question_index': current_q_index}
        )
    
    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Traite la réponse de l'utilisateur"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        session = user_sessions.get(user_id)
        
        if not session:
            await query.edit_message_text("❌ Session expirée. Tapez /quiz pour recommencer.")
            return
        
        # Extraire la réponse
        try:
            answer_index = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            await query.edit_message_text("❌ Erreur dans la réponse. Tapez /quiz pour recommencer.")
            return
        
        current_q_index = session['current_question']
        question = session['questions'][current_q_index]
        
        # Calculer le temps de réponse
        response_time = time.time() - session['question_start_time']
        is_correct = answer_index == question['correct']
        
        # Calculer les points avec bonus vitesse ajusté pour 10 secondes
        points = 0
        if is_correct:
            points = 10
            if response_time < 5:  # Bonus vitesse pour réponse < 5 secondes (au lieu de 10)
                points += 5
        
        session['score'] += points
        
        # Créer le message de résultat
        if is_correct:
            result_text = "✅ **Excellente réponse !** 🎉\n"
            if response_time < 5:  # Bonus vitesse ajusté
                result_text += f"⚡ **Bonus vitesse !** ({response_time:.1f}s)\n"
            else:
                result_text += f"⏰ Temps: {response_time:.1f}s\n"
        else:
            result_text = "❌ **Dommage !** 😔\n"
            result_text += f"💡 La bonne réponse était: **{question['options'][question['correct']]}**\n"
            result_text += f"⏰ Temps: {response_time:.1f}s\n"
        
        result_text += f"\n💰 **Points gagnés:** +{points}\n"
        result_text += f"🏆 **Score total:** {session['score']} points\n"
        result_text += f"📊 **Progression:** {current_q_index + 1}/15"
        
        await query.edit_message_text(result_text, parse_mode='Markdown')
        
        # Question suivante
        session['current_question'] += 1
        await asyncio.sleep(3)  # Pause de 3 secondes
        await self.send_question(update, context, user_id)
    
    async def question_timeout(self, context: ContextTypes.DEFAULT_TYPE):
        """Gère l'expiration d'une question"""
        job_data = context.job.data
        user_id = job_data['user_id']
        question_index = job_data['question_index']
        
        session = user_sessions.get(user_id)
        if not session or session['current_question'] != question_index:
            return
        
        # Timeout
        question = session['questions'][question_index]
        timeout_text = f"⏰ **Temps écoulé !** ⏰\n\n"
        timeout_text += f"💡 La bonne réponse était: **{question['options'][question['correct']]}**\n"
        timeout_text += f"🏆 Score actuel: {session['score']} points"
        
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=timeout_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Erreur timeout: {e}")
        
        session['current_question'] += 1
        await asyncio.sleep(2)
        
        # Question suivante
        fake_update = type('obj', (object,), {
            'effective_chat': type('obj', (object,), {'id': user_id}),
            'effective_user': type('obj', (object,), {'id': user_id})
        })()
        
        await self.send_question(fake_update, context, user_id)
    
    async def end_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Termine le quiz et affiche le score final"""
        session = user_sessions.get(user_id)
        if not session:
            return
        
        total_time = time.time() - session['start_time']
        score = session['score']
        max_score = len(session['questions']) * 15  # 10 + 5 bonus max par question
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        
        # Déterminer le rang selon le pourcentage avec plus de niveaux
        if percentage >= 95:
            rank = "👑 **Maître Otaku Légendaire Ultime**"
            emoji = "🌟"
        elif percentage >= 90:
            rank = "🏆 **Maître Otaku Légendaire**"
            emoji = "👑"
        elif percentage >= 80:
            rank = "⭐ **Expert Anime**"
            emoji = "🔥"
        elif percentage >= 60:
            rank = "🎖️ **Fan Confirmé**"
            emoji = "⚡"
        elif percentage >= 40:
            rank = "📚 **Amateur Éclairé**"
            emoji = "💪"
        else:
            rank = "🌱 **Apprenti Otaku**"
            emoji = "🎯"
        
        username = update.effective_user.first_name or "Otaku"
        
        final_text = f"""
🎊 **Quiz terminé, {username} !** 🎊

{emoji} **RÉSULTATS FINAUX** {emoji}

🏆 **Score:** {score}/{max_score} points
📈 **Réussite:** {percentage:.1f}%
⏱️ **Temps total:** {total_time/60:.1f} minutes
🎭 **Rang obtenu:** {rank}

📊 **Statistiques détaillées:**
- Questions traitées: {len(session['questions'])}
- Temps moyen/question: {total_time/len(session['questions']):.1f}s
- Efficacité: {"🔥 Excellent" if percentage >= 80 else "👍 Bien" if percentage >= 60 else "💪 À améliorer"}

🎮 **Prêt pour un nouveau défi ?** Tapez /quiz !
📚 **Besoin d'aide ?** Tapez /help

Merci d'avoir joué ! 🎌✨
        """
        
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=final_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Erreur fin de quiz: {e}")
        
        # Nettoyer la session
        if user_id in user_sessions:
            del user_sessions[user_id]
    
    async def show_score(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Affiche le score actuel si un quiz est en cours"""
        user_id = update.effective_user.id
        session = user_sessions.get(user_id)
        
        if not session:
            await update.message.reply_text(
                "❌ **Aucun quiz en cours !**\n\n🎯 Tapez /quiz pour commencer votre aventure anime ! 🎌", 
                parse_mode='Markdown'
            )
            return
        
        current_q = session['current_question']
        total_q = len(session['questions'])
        score = session['score']
        elapsed_time = (time.time() - session['start_time']) / 60
        
        status_text = f"""
📊 **Quiz en cours** 📊

🎯 **Progression:** {current_q}/{total_q} questions
🏆 **Score actuel:** {score} points
⏱️ **Temps écoulé:** {elapsed_time:.1f} minutes
🔥 **Statut:** {"🚀 En feu !" if score >= current_q * 10 else "💪 Continue !"}

⚡ **Prochaine question arrive...**
        """
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /help"""
        help_text = """
🆘 **Guide du Quiz Anime** 🆘

**🎮 Comment jouer :**
1️⃣ Tapez /quiz pour commencer
2️⃣ Répondez aux 15 questions via les boutons
3️⃣ Chaque question a 10 secondes
4️⃣ Gagnez des points et déverrouillez votre rang !

**🏆 Système de points :**
- ✅ Bonne réponse : 10 points
- ⚡ Bonus vitesse : +5 points (< 5 secondes)
- ❌ Mauvaise réponse : 0 point

**🎭 Types de questions :**
- 📝 **Texte** - Culture otaku mondiale
- 🖼️ **Images** - Personnages iconiques (Wikia officiels)
- 🎵 **Openings** - Musiques légendaires (YouTube authentiques)

**💎 Niveaux de difficulté :**
- 🟢 **Facile** - Anime populaires (Naruto, One Piece...)
- 🟡 **Moyen** - Connaissances générales  
- 🔴 **Difficile** - Pour les vrais fans
- 💜 **Cauchemar** - Références cultes
- 🖤 **Impossible** - Niveau maître absolu

**🏅 Rangs disponibles :**
- 🌟 Maître Otaku Légendaire Ultime (95%+)
- 👑 Maître Otaku Légendaire (90%+)
- 🔥 Expert Anime (80%+)
- ⚡ Fan Confirmé (60%+)
- 💪 Amateur Éclairé (40%+)
- 🎯 Apprenti Otaku (<40%)

**🌍 Animes inclus :**
- **Classiques :** Naruto, One Piece, Dragon Ball, Death Note, Evangelion
- **Modernes :** Demon Slayer, Jujutsu Kaisen, Attack on Titan, My Hero Academia
- **Cultes :** Cowboy Bebop, Steins;Gate, Hunter x Hunter
- **Films :** Your Name, Studio Ghibli
- **Et bien plus !**

**🎭 Niveaux de difficulté :**
- 🟢 **Facile** - Anime populaires (Naruto, One Piece...)
- 🟡 **Moyen** - Connaissances générales
- 🔴 **Difficile** - Pour les vrais experts !

**🏅 Rangs disponibles :**
- 👑 Maître Otaku Légendaire (90%+)
- ⭐ Expert Anime (80%+)
- 🎖️ Fan Confirmé (60%+)
- 📚 Amateur Éclairé (40%+)
- 🌱 Apprenti Otaku (<40%)

**📋 Commandes utiles :**
- /quiz - Nouveau quiz
- /score - Score actuel
- /start - Retour à l'accueil
- /help - Cette aide

🎌 **Bon quiz et que le meilleur otaku gagne !** 🎌
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    def run(self):
        """Lance le bot"""
        logger.info("🤖 Quiz Anime Bot démarré sur Railway !")
        self.app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    bot = AnimeQuizBot(BOT_TOKEN)
    bot.run()
