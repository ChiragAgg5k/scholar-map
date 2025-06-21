"""Sample Data Manager for Scholar Map"""

import uuid
from datetime import datetime, timedelta
from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.text import Text

from src.models.paper import Paper
from src.mindsdb_manager import MindsDBManager

console = Console()


def create_sample_papers() -> List[Paper]:
    """Create a list of sample research papers"""

    # Generate dates for the last 2 years
    base_date = datetime.now()

    sample_papers = [
        Paper(
            paper_id=str(uuid.uuid4()),
            title="Attention Is All You Need: A Comprehensive Study of Transformer Architecture",
            authors="Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, L., Polosukhin, I.",
            category="cs.LG",
            pub_date=(base_date - timedelta(days=365)).strftime("%Y-%m-%d"),
            arxiv_id="1706.03762",
            journal="Neural Information Processing Systems (NeurIPS)",
            research_field="Natural Language Processing",
            paper_type="Conference Paper",
            citation_count=45230,
            abstract="The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train.",
            summary="This paper introduces the Transformer architecture, which uses attention mechanisms instead of recurrence or convolutions for sequence transduction. The model achieves superior performance on machine translation tasks while being more parallelizable and faster to train than previous approaches.",
        ),
        Paper(
            paper_id=str(uuid.uuid4()),
            title="BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            authors="Devlin, J., Chang, M.W., Lee, K., Toutanova, K.",
            category="cs.CL",
            pub_date=(base_date - timedelta(days=300)).strftime("%Y-%m-%d"),
            arxiv_id="1810.04805",
            journal="Conference of the North American Chapter of the Association for Computational Linguistics (NAACL)",
            research_field="Natural Language Processing",
            paper_type="Conference Paper",
            citation_count=38560,
            abstract="We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks.",
            summary="BERT introduces bidirectional pre-training for language understanding, enabling fine-tuning with minimal additional layers to achieve state-of-the-art performance across various NLP tasks.",
        ),
        Paper(
            paper_id=str(uuid.uuid4()),
            title="Generative Adversarial Networks",
            authors="Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., Bengio, Y.",
            category="cs.LG",
            pub_date=(base_date - timedelta(days=450)).strftime("%Y-%m-%d"),
            arxiv_id="1406.2661",
            journal="Advances in Neural Information Processing Systems (NIPS)",
            research_field="Machine Learning",
            paper_type="Conference Paper",
            citation_count=52340,
            abstract="We propose a new framework for estimating generative models via an adversarial process, in which we simultaneously train two models: a generative model G that captures the data distribution, and a discriminative model D that estimates the probability that a sample came from the training data rather than G. The training procedure for G is to maximize the probability of D making a mistake. This framework corresponds to a minimax two-player game.",
            summary="GANs introduce an adversarial training framework with a generator and discriminator competing in a minimax game, enabling high-quality generative modeling across various domains.",
        ),
        Paper(
            paper_id=str(uuid.uuid4()),
            title="ResNet: Deep Residual Learning for Image Recognition",
            authors="He, K., Zhang, X., Ren, S., Sun, J.",
            category="cs.CV",
            pub_date=(base_date - timedelta(days=500)).strftime("%Y-%m-%d"),
            arxiv_id="1512.03385",
            journal="IEEE Conference on Computer Vision and Pattern Recognition (CVPR)",
            research_field="Computer Vision",
            paper_type="Conference Paper",
            citation_count=89230,
            abstract="Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize.",
            summary="ResNet introduces residual connections that enable training of much deeper networks by learning residual functions, significantly improving image recognition performance.",
        ),
        Paper(
            paper_id=str(uuid.uuid4()),
            title="GPT-3: Language Models are Few-Shot Learners",
            authors="Brown, T.B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A.",
            category="cs.CL",
            pub_date=(base_date - timedelta(days=200)).strftime("%Y-%m-%d"),
            arxiv_id="2005.14165",
            journal="Advances in Neural Information Processing Systems (NeurIPS)",
            research_field="Natural Language Processing",
            paper_type="Conference Paper",
            citation_count=28450,
            abstract="Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. While typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples. By contrast, humans can generally perform a new language task from only a few examples or from simple instructions.",
            summary="GPT-3 demonstrates that large language models can perform new tasks with minimal examples through few-shot learning, reducing the need for extensive fine-tuning datasets.",
        ),
        Paper(
            paper_id=str(uuid.uuid4()),
            title="You Only Look Once: Unified, Real-Time Object Detection",
            authors="Redmon, J., Divvala, S., Girshick, R., Farhadi, A.",
            category="cs.CV",
            pub_date=(base_date - timedelta(days=600)).strftime("%Y-%m-%d"),
            arxiv_id="1506.02640",
            journal="IEEE Conference on Computer Vision and Pattern Recognition (CVPR)",
            research_field="Computer Vision",
            paper_type="Conference Paper",
            citation_count=31200,
            abstract="We present YOLO, a new approach to object detection. Prior work on object detection repurposes classifiers to perform detection. Instead, we frame object detection as a regression problem to spatially separated bounding boxes and associated class probabilities. A single neural network predicts bounding boxes and class probabilities directly from full images in one evaluation.",
            summary="YOLO frames object detection as a regression problem, enabling real-time detection with a single neural network evaluation, significantly improving speed over previous approaches.",
        ),
        Paper(
            paper_id=str(uuid.uuid4()),
            title="Neural Information Retrieval: At the End of the Early Years",
            authors="Mitra, B., Craswell, N.",
            category="cs.IR",
            pub_date=(base_date - timedelta(days=150)).strftime("%Y-%m-%d"),
            arxiv_id="1805.09713",
            journal="Information Retrieval Journal",
            research_field="Artificial Intelligence",
            paper_type="Review Paper",
            citation_count=1230,
            abstract="Neural ranking models for information retrieval (IR) use shallow or deep neural networks to rank search results in response to a query. Traditional learning to rank models employ supervised machine learning over hand-crafted IR features. By contrast, neural models learn representations of language from raw text that can bridge the gap between query and document vocabulary.",
            summary="This review discusses neural ranking models for information retrieval, highlighting how they learn language representations from raw text to improve search result ranking.",
        ),
        Paper(
            paper_id=str(uuid.uuid4()),
            title="Federated Learning: Challenges, Methods, and Future Directions",
            authors="Li, T., Sahu, A.K., Talwalkar, A., Smith, V.",
            category="cs.LG",
            pub_date=(base_date - timedelta(days=100)).strftime("%Y-%m-%d"),
            arxiv_id="1908.07873",
            journal="IEEE Signal Processing Magazine",
            research_field="Machine Learning",
            paper_type="Review Paper",
            citation_count=8940,
            abstract="Federated learning (FL) is a machine learning setting where many clients (e.g., mobile devices or whole organizations) collaboratively train a model under the orchestration of a central server, while keeping the training data decentralized. This approach enables multiple actors to build a common, robust machine learning model without sharing data, thus addressing critical issues such as data privacy.",
            summary="Federated learning enables collaborative model training across decentralized clients while preserving data privacy, addressing critical concerns in distributed machine learning.",
        ),
        Paper(
            paper_id=str(uuid.uuid4()),
            title="Quantum Machine Learning: What Quantum Computing Means to Data Mining",
            authors="Biamonte, J., Wittek, P., Pancotti, N., Rebentrost, P., Wiebe, N., Lloyd, S.",
            category="physics",
            pub_date=(base_date - timedelta(days=80)).strftime("%Y-%m-%d"),
            arxiv_id="1611.09347",
            journal="Nature",
            research_field="Data Science",
            paper_type="Journal Article",
            citation_count=2150,
            abstract="Quantum machine learning is an emerging interdisciplinary research area at the intersection of quantum physics and machine learning. The most common use of the term refers to machine learning algorithms for the analysis of classical data executed on a quantum computer. This includes hybrid methods that involve both classical and quantum processing.",
            summary="This paper explores quantum machine learning at the intersection of quantum physics and ML, focusing on algorithms for classical data analysis on quantum computers.",
        ),
        Paper(
            paper_id=str(uuid.uuid4()),
            title="Explainable AI: Interpreting, Explaining and Visualizing Deep Learning",
            authors="Samek, W., Montavon, G., Vedaldi, A., Hansen, L.K., Müller, K.R.",
            category="cs.AI",
            pub_date=(base_date - timedelta(days=50)).strftime("%Y-%m-%d"),
            arxiv_id="1910.10045",
            journal="Springer Nature",
            research_field="Artificial Intelligence",
            paper_type="Journal Article",
            citation_count=3420,
            abstract="The development of 'intelligent' systems that can take decisions and perform actions autonomously and without constant human oversight is progressing rapidly. However, a key component of intelligent systems is currently lagging behind: the ability to explain decisions to users and stakeholders. This book addresses this challenge by providing a comprehensive introduction to interpretable machine learning.",
            summary="This book addresses the challenge of explainable AI by providing comprehensive methods for interpreting and explaining deep learning decisions to users and stakeholders.",
        ),
    ]

    return sample_papers


def display_sample_papers(papers: List[Paper]):
    """Display the sample papers in a formatted way"""
    console.print("\n[bold cyan]Sample Research Papers Preview:[/bold cyan]")
    console.print(f"[dim]Total papers available: {len(papers)}[/dim]\n")

    for i, paper in enumerate(papers[:5], 1):  # Show first 5 papers
        preview_panel = Panel(
            f"[bold]Title:[/bold] {paper.title}\n"
            f"[bold]Authors:[/bold] {paper.authors[:80]}{'...' if len(paper.authors) > 80 else ''}\n"
            f"[bold]Category:[/bold] {paper.category}\n"
            f"[bold]Research Field:[/bold] {paper.research_field}\n"
            f"[bold]Citations:[/bold] {paper.citation_count:,}\n"
            f"[bold]Abstract:[/bold] {paper.abstract[:150]}{'...' if len(paper.abstract) > 150 else ''}",
            title=f"Sample Paper {i}",
            border_style="blue",
            padding=(1, 2),
        )
        console.print(preview_panel)

    if len(papers) > 5:
        console.print(f"[dim]... and {len(papers) - 5} more papers[/dim]")


def insert_sample_papers(db_manager: MindsDBManager) -> bool:
    """Insert sample papers into the database"""
    try:
        # Create sample papers
        sample_papers = create_sample_papers()

        # Display header
        header_text = Text("Sample Data Insertion", style="bold magenta")
        header_panel = Panel(
            header_text,
            subtitle="Insert pre-defined research papers for testing and demonstration",
            border_style="magenta",
            padding=(1, 2),
        )
        console.print(header_panel)

        # Show preview of sample papers
        display_sample_papers(sample_papers)

        # Ask for confirmation
        console.print()
        if not Confirm.ask(
            f"[bold yellow]Do you want to insert these {len(sample_papers)} sample papers into the knowledge base?[/bold yellow]",
            default=True,
        ):
            console.print("[yellow]Sample data insertion cancelled.[/yellow]")
            return False

        # Insert papers using direct insert query
        console.print(
            f"\n[bold cyan]Inserting {len(sample_papers)} sample papers...[/bold cyan]"
        )

        try:
            from rich.progress import Progress, SpinnerColumn, TextColumn

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(
                    "Processing and inserting papers into knowledge base...",
                    total=len(sample_papers),
                )

                for paper in sample_papers:
                    insert_query = f"""
                    INSERT INTO research_papers_kb 
                    (paper_id, title, authors, category, pub_date, arxiv_id, journal, research_field, paper_type, citation_count, abstract, summary)
                    VALUES (
                        '{paper.paper_id}',
                        '{paper.title.replace("'", "''")}',
                        '{paper.authors.replace("'", "''")}',
                        '{paper.category}',
                        '{paper.pub_date}',
                        '{paper.arxiv_id}',
                        '{paper.journal.replace("'", "''")}',
                        '{paper.research_field}',
                        '{paper.paper_type}',
                        {paper.citation_count},
                        '{paper.abstract.replace("'", "''")}',
                        '{paper.summary.replace("'", "''")}'
                    )
                    """

                    query = db_manager.server.query(insert_query)
                    query.fetch()
                    progress.advance(task)

            success = True
        except Exception as e:
            console.print(f"[red]Error during insertion: {str(e)}[/red]")
            success = False

        if success:
            success_panel = Panel(
                f"[bold green]Sample Data Inserted Successfully![/bold green]\n\n"
                f"Successfully inserted {len(sample_papers)} sample research papers.\n"
                f"These papers span multiple research fields including:\n"
                f"• Machine Learning & AI\n"
                f"• Computer Vision\n"
                f"• Natural Language Processing\n"
                f"• Data Science\n\n"
                f"[dim]You can now test search and analysis features with this data.[/dim]",
                title="Operation Complete",
                border_style="green",
                padding=(1, 2),
            )
            console.print(success_panel)
            return True
        else:
            console.print(
                "[red]Failed to insert sample papers. Please check the error messages above.[/red]"
            )
            return False

    except Exception as e:
        error_panel = Panel(
            f"[bold red]Sample Data Insertion Failed[/bold red]\n\n"
            f"An unexpected error occurred while inserting sample papers.\n\n"
            f"[dim]Error details: {str(e)}[/dim]",
            title="Error",
            border_style="red",
            padding=(1, 2),
        )
        console.print(error_panel)
        return False


if __name__ == "__main__":
    """Main execution when script is run directly"""
    # Initialize manager and console
    manager = MindsDBManager()

    # Display welcome message
    welcome_text = Text("Scholar Map - Sample Data Manager", style="bold blue")
    welcome_panel = Panel(
        welcome_text,
        subtitle="Insert sample research papers for testing and demonstration",
        border_style="blue",
        padding=(1, 2),
    )
    console.print(welcome_panel)

    # Connect to database
    if manager.connect() is False:
        console.print("[red]Failed to connect to MindsDB. Exiting.[/red]")
        exit(1)

    # Insert sample papers
    try:
        insert_sample_papers(manager)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user (Ctrl+C)[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {str(e)}[/red]")
