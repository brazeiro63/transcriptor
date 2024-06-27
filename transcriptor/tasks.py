from textwrap import dedent

from crewai import Task  # type: ignore


class PreachDefiningTasks:
    def dedication_task(self, agent, bible_verse):
        return Task(
            description=dedent(f"""\
            Retrieve the given verse: {bible_verse}.
            Infer a target audience for a preaching about the verse.

            Formulate a reading dedication for this target audience,
            and the tribulations they may be going though.

            Keep in mind that the target audience you intend to reach
            has lower income and a lower level of education.
            """),
            expected_output=dedent("""\
                Description of the target audience for de verse and
                a reading dedications for this audience.
            """),
            agent=agent,
            bible_verse=bible_verse,
        )

    def preach_development_task(self, agent, bible_verse):
        return Task(
            description=dedent(f"""\
            Create a preaching about the verse: {bible_verse}.

            Ensure to use from 350 up to 400 words.
            Aim the preaching to the target audience.
            """),
            agent=agent,
            bible_verse=bible_verse,
            expected_output=dedent("""\
                A text for a preaching aiming that audience.
            """),
        )

    def preach_format_task(self, agent, bible_verse):
        return Task(
            description=dedent(f"""\
            Review the target audience, the reading dedication, and
            the preaching texts.

            Your final answer MUST include BOTH all target audience
            and reading dedication for {bible_verse}, and the preaching.
            """),
            agent=agent,
            bible_verse=bible_verse,
            expected_output=dedent(f"""\
                A document writen in brazilian portuguese (pt-BR)
                that MUST contain:
                    the text os the verse {bible_verse};
                    the reading dedication; and
                    the text for the preaching.
                Must not be signed.
            """),
        )


class VideoStoryTellingTasks:
    def storytelling_task(self, agent, preaching):
        return Task(
            description=dedent(f"""\
            Develop 16x9, photo-realistic image prompts that will visually
            represent the text: {preaching}.

            The idea is that they are images with a religious background,
            with an impact that makes the viewer want to watch the video.

            The images must be related to what is being said in the text.
            Images should be inspiring and emotional.

            You should create the prompts as follows:
            they must all be in English;
            all numbers MUST be writen in full;
            all prompts MUST end with “ realistic photography style,
            16x9, -ar 16:09”;
            they must be specific and detailed, as they will be used
            in a “text to image” generator;
            you must describe in detail what atmosphere and feeling the
            image should convey.

            All images with a character must be accompanied by the figure
            of Jesus, representing divine protection.

            Maintain consistency of characteristics and style in ALL
            PROMPTS according to character characteristics, colors and
            composition.

            Write which sentence in the text the scene fits into.

            Make a table with the scene number, corresponding text,
            and full prompt.

            Represent the text with images related to:
            a) scenarios: nature, gardens, libraries, churches, ocean,
            lakes and flowers.
            b) religious: scenes of doves, image of Jesus Christ,
            rays of light, illuminated clouds.
            c) objects: Candles, books, Bibles, flowers, raindrops
            on leaves or flowers, cups of tea.
            d) people: hands in prayer, expressive eyes, people
            meditating, serene faces, hair touched by the wind,
            manifestations of affection.
            """),
            agent=agent,
            preaching=preaching,
            expected_output=dedent("""\
                A script for a YouTube video, in table form, which
                MUST contain:
                    the scene number;
                    the prompt for image generation;
                    the description of the scene;
                    the text corresponding to the scene.
            """),
        )
