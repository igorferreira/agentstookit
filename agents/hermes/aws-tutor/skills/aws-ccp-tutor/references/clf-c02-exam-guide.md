# AWS Certified Cloud Practitioner (CLF-C02) — Exam Guide

Fonte: exam guide oficial da AWS (docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/). Conteúdo reproduzido fielmente para uso como material de referência de ensino — não parafraseie de forma a perder precisão técnica.

## Público-alvo

Candidato com até 6 meses de exposição à AWS Cloud (design, implementação e/ou operação). Fora de escopo para o candidato: coding, design de arquitetura de nuvem, troubleshooting, implementação, teste de carga/performance.

O exame valida a capacidade de:
- Explicar o valor da AWS Cloud
- Entender e explicar o AWS Shared Responsibility Model
- Entender o AWS Well-Architected Framework
- Entender boas práticas de segurança
- Entender custos, economia e práticas de billing da AWS Cloud
- Descrever e posicionar os serviços core da AWS (compute, network, database, storage)
- Identificar serviços AWS para casos de uso comuns

## Formato do exame

- 65 perguntas: 50 valem nota, 15 são piloto não identificadas (não afetam a nota)
- Tipos de pergunta: **multiple choice** (1 resposta certa, 3 distratores) e **multiple response** (2+ respostas certas entre 5+ opções)
- 90 minutos (não-nativos em inglês podem pedir +30 min)
- Sem penalidade por errar — pergunta em branco conta como errada
- Nota: escala 100–1000, aprovação em **700**
- Modelo **compensatório**: não precisa passar em cada seção, só na média geral. O relatório de resultado mostra desempenho por seção, mas isso é só informativo.
- Custo: US$ 100. Validade: 3 anos (renovável passando a versão atual do exame ou qualquer exame Associate/Professional)

## Domínios e pesos

| Domínio | Peso |
|---|---|
| 1. Cloud Concepts | 24% |
| 2. Security and Compliance | 30% |
| 3. Cloud Technology and Services | 34% |
| 4. Billing, Pricing, and Support | 12% |

---

## Domínio 1: Cloud Concepts (24%)

### Task Statement 1.1 — Define the benefits of the AWS Cloud
**Knowledge:** proposta de valor da AWS Cloud.
**Skills:** entender os benefícios da infraestrutura global (velocidade de deploy, alcance global); entender as vantagens de alta disponibilidade, elasticidade e agilidade.

### Task Statement 1.2 — Identify design principles of the AWS Cloud
**Knowledge:** AWS Well-Architected Framework.
**Skills:** entender os 6 pilares (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability); identificar diferenças entre os pilares.

### Task Statement 1.3 — Understand the benefits of and strategies for migration to the AWS Cloud
**Knowledge:** estratégias de adoção de cloud; recursos de apoio à jornada de migração.
**Skills:** entender os componentes do AWS Cloud Adoption Framework (AWS CAF) — redução de risco de negócio, melhoria de ESG, aumento de receita, aumento de eficiência operacional; identificar estratégias de migração apropriadas (ex.: replicação de banco de dados, uso do AWS Snowball — os "7 Rs" de migração).

### Task Statement 1.4 — Understand concepts of cloud economics
**Knowledge:** aspectos da economia de cloud; economia gerada pela migração para a nuvem.
**Skills:** entender custo fixo vs. variável; custos associados a ambientes on-premises; diferenças entre estratégias de licenciamento (BYOL vs. licença inclusa); conceito de rightsizing; benefícios de automação; economia de escala.

---

## Domínio 2: Security and Compliance (30% — maior peso individual)

### Task Statement 2.1 — Understand the AWS shared responsibility model
**Knowledge:** AWS Shared Responsibility Model.
**Skills:** reconhecer os componentes do modelo; descrever responsabilidades do cliente; descrever responsabilidades da AWS; descrever responsabilidades compartilhadas; entender como as responsabilidades mudam conforme o serviço usado (ex.: Amazon RDS, AWS Lambda, Amazon EC2).

### Task Statement 2.2 — Understand AWS Cloud security, governance, and compliance concepts
**Knowledge:** conceitos de compliance e governança AWS; benefícios de segurança em nuvem (ex.: criptografia); onde capturar/localizar logs de segurança.
**Skills:** identificar onde achar informação de compliance (ex.: AWS Artifact); entender necessidades de compliance por localização geográfica/indústria; descrever como o cliente protege recursos na AWS (Amazon Inspector, AWS Security Hub, Amazon GuardDuty, AWS Shield); identificar opções de criptografia (em trânsito, em repouso); reconhecer serviços de governança/compliance (monitoramento com Amazon CloudWatch; auditoria com AWS CloudTrail, AWS Audit Manager, AWS Config; relatórios de acesso); reconhecer que requisitos de compliance variam entre serviços.

### Task Statement 2.3 — Identify AWS access management capabilities
**Knowledge:** IAM; importância de proteger a conta root; princípio do menor privilégio; AWS IAM Identity Center (antigo AWS SSO).
**Skills:** entender access keys, políticas de senha e armazenamento de credenciais (AWS Secrets Manager, AWS Systems Manager); identificar métodos de autenticação (MFA, IAM Identity Center, IAM roles cross-account); definir grupos, usuários, políticas custom e gerenciadas seguindo menor privilégio; identificar tarefas que só o root user pode executar; entender métodos de proteção do root user; entender tipos de gestão de identidade (ex.: federada).

### Task Statement 2.4 — Identify components and resources for security
**Knowledge:** capacidades de segurança que a AWS fornece; documentação de segurança da AWS.
**Skills:** descrever features/serviços de segurança (AWS WAF, AWS Firewall Manager, AWS Shield, Amazon GuardDuty); entender que produtos de segurança de terceiros existem no AWS Marketplace; identificar onde achar informação de segurança (AWS Knowledge Center, AWS Security Center, AWS Security Blog); entender o uso de serviços como o AWS Trusted Advisor para identificar problemas de segurança.

---

## Domínio 3: Cloud Technology and Services (34% — maior domínio)

### Task Statement 3.1 — Define methods of deploying and operating in the AWS Cloud
**Knowledge:** formas de provisionar e operar na AWS Cloud; formas de acessar serviços AWS; modelos de deployment em nuvem.
**Skills:** decidir entre acesso programático (APIs, SDKs, CLI), AWS Management Console e infrastructure as code (IaC); avaliar se usar operações pontuais ou processos repetíveis; identificar modelos de deployment (cloud, híbrido, on-premises).

### Task Statement 3.2 — Define the AWS global infrastructure
**Knowledge:** Regions, Availability Zones e edge locations; alta disponibilidade; uso de múltiplas Regions; benefícios de edge locations.
**Skills:** descrever a relação entre Regions, AZs e edge locations; descrever como atingir alta disponibilidade usando múltiplas AZs; reconhecer que AZs não compartilham pontos únicos de falha; descrever quando usar múltiplas Regions (disaster recovery, continuidade de negócio, baixa latência para usuários finais, soberania de dados).

### Task Statement 3.3 — Identify AWS compute services
**Skills:** reconhecer o uso apropriado de tipos de instância EC2 (compute optimized, storage optimized etc.); reconhecer o uso apropriado de opções de container (Amazon ECS, Amazon EKS); reconhecer o uso apropriado de opções serverless (AWS Fargate, AWS Lambda); reconhecer que auto scaling provê elasticidade; identificar o propósito de load balancers.

### Task Statement 3.4 — Identify AWS database services
**Knowledge:** serviços de banco de dados AWS; migração de banco de dados.
**Skills:** decidir entre bancos hospedados em EC2 ou bancos gerenciados AWS; identificar bancos relacionais (Amazon RDS, Amazon Aurora); identificar bancos NoSQL (Amazon DynamoDB); identificar bancos em memória (Amazon ElastiCache); identificar ferramentas de migração de banco (AWS DMS, AWS SCT).

### Task Statement 3.5 — Identify AWS network services
**Skills:** identificar componentes de uma VPC (subnets, gateways); entender segurança em VPC (network ACLs, security groups, Amazon Inspector); entender o propósito do Amazon Route 53; identificar opções de conectividade de rede à AWS (AWS VPN, AWS Direct Connect).

### Task Statement 3.6 — Identify AWS storage services
**Skills:** identificar usos de object storage; reconhecer diferenças entre classes de armazenamento do Amazon S3; identificar soluções de block storage (Amazon EBS, instance store); identificar serviços de arquivos (Amazon EFS, Amazon FSx); identificar sistemas de arquivo com cache (AWS Storage Gateway); entender casos de uso de lifecycle policies; entender casos de uso do AWS Backup.

### Task Statement 3.7 — Identify AWS AI/ML services and analytics services
**Skills:** entender serviços de AI/ML e o que eles fazem (Amazon SageMaker AI, Amazon Lex, Amazon Kendra); identificar serviços de analytics de dados (Amazon Athena, Amazon Kinesis, AWS Glue, Amazon QuickSight).

### Task Statement 3.8 — Identify services from other in-scope AWS service categories
**Knowledge:** serviços de integração de aplicações (Amazon EventBridge, Amazon SNS, Amazon SQS); serviços de aplicação de negócio (Amazon Connect, Amazon SES); serviços de customer enablement (AWS Support); ferramentas de desenvolvedor (AWS CodeBuild, AWS CodePipeline, AWS X-Ray); end-user computing (Amazon AppStream 2.0, Amazon WorkSpaces, WorkSpaces Secure Browser); frontend web e mobile (AWS Amplify, AWS AppSync); IoT (AWS IoT Core).
**Skills:** escolher o serviço apropriado para entregar mensagens e enviar alertas/notificações; escolher o serviço apropriado para necessidades de aplicação de negócio; escolher a opção apropriada de suporte a negócio; identificar ferramentas para desenvolver/deployar/debugar aplicações; identificar serviços que apresentam saída de VMs em máquinas de usuário final; identificar serviços para criar/deployar frontend e mobile; identificar serviços que gerenciam dispositivos IoT.

---

## Domínio 4: Billing, Pricing, and Support (12%)

### Task Statement 4.1 — Compare AWS pricing models
**Knowledge:** opções de compra de compute (On-Demand, Reserved Instances, Spot Instances, AWS Savings Plans, Dedicated Hosts, Dedicated Instances, Capacity Reservations); opções e tiers de storage.
**Skills:** identificar quando usar cada opção de compra de compute; descrever a flexibilidade de Reserved Instances; descrever o comportamento de Reserved Instances em AWS Organizations; entender custo de transferência de dados de entrada e saída (entre Regions, dentro da mesma Region); entender preços de opções/tiers de storage.

### Task Statement 4.2 — Understand resources for billing, budget, and cost management
**Knowledge:** suporte e informação de billing; informação de preços dos serviços AWS; AWS Organizations; cost allocation tags.
**Skills:** entender usos e capacidades do AWS Budgets e AWS Cost Explorer; entender usos e capacidades da AWS Pricing Calculator; entender consolidated billing e alocação de custos no AWS Organizations; entender tipos de cost allocation tags e sua relação com relatórios de billing (AWS Cost and Usage Report).

### Task Statement 4.3 — Identify AWS technical resources and AWS Support options
**Knowledge:** recursos e documentação nos sites oficiais da AWS; planos de AWS Support; papel da AWS Partner Network (ISVs e system integrators); AWS Support Center.
**Skills:** localizar whitepapers, blogs e documentação nos sites oficiais da AWS; identificar e localizar recursos técnicos (AWS Prescriptive Guidance, AWS Knowledge Center, AWS re:Post); identificar opções de suporte AWS para clientes (comunidades, AWS Developer Support, AWS Business Support, AWS Enterprise On-Ramp Support, AWS Enterprise Support); identificar o papel do AWS Trusted Advisor, AWS Health Dashboard e AWS Health API para gestão/monitoramento de ambientes visando otimização de custo; identificar o papel do time AWS Trust and Safety para reportar abuso de recursos AWS; entender o papel dos AWS Partners (AWS Marketplace, ISVs, system integrators); identificar benefícios de ser um AWS Partner (treinamento e certificação, eventos, descontos de volume); identificar serviços-chave oferecidos pelo AWS Marketplace (cost management, governança e entitlement); identificar opções de assistência técnica disponíveis na AWS (AWS Professional Services, AWS Solutions Architects).
