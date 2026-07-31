$ErrorActionPreference = "Stop"

$root = Resolve-Path "."
$upstream = Join-Path $root "tests\corpus\upstream"
New-Item -ItemType Directory -Force $upstream | Out-Null
Set-Location $upstream

function Clone-Sparse {
    param(
        [string]$Url,
        [string]$Directory,
        [string[]]$Paths
    )

    if (-not (Test-Path $Directory)) {
        git clone --depth 1 --filter=blob:none --sparse $Url $Directory
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to clone $Url"
    }

    if ($Paths.Count -gt 0) {
        git -C $Directory sparse-checkout set -- $Paths
        if ($LASTEXITCODE -ne 0) {
            throw "Failed sparse checkout for $Directory"
        }
    }
}

function Clone-Shallow {
    param(
        [string]$Url,
        [string]$Directory
    )

    if (-not (Test-Path $Directory)) {
        git clone --depth 1 $Url $Directory
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to clone $Url"
    }
}

# 1. ADR 正文：Backstage
Clone-Sparse `
    "https://github.com/backstage/backstage.git" `
    "backstage" `
    @("docs/architecture-decisions")

# 2. ADR 模板、示例与许可：MADR
Clone-Shallow `
    "https://github.com/adr/madr.git" `
    "madr"

# 3. ADR corpus 与职责边界说明：Mozilla SRE ADRs（已归档，只读）
Clone-Shallow `
    "https://github.com/mozilla/sre-adrs.git" `
    "mozilla-sre-adrs"

# # 4. 技术提案、测试计划、升级回退与毕业条件：Kubernetes KEP
# Clone-Sparse `
#     "https://github.com/kubernetes/enhancements.git" `
#     "kubernetes-enhancements" `
#     @(
#         "keps/README.md",
#         "keps/NNNN-kep-template",
#         "keps/sig-node/127-user-namespaces",
#         "keps/sig-api-machinery/555-server-side-apply"
#     )

# 5. 技术提案与 rejected-but-well-written 边界案例：Python PEP
# Clone-Sparse `
#     "https://github.com/python/peps.git" `
#     "python-peps" `
#     @("peps/pep-2026.rst", "LICENSE")

# 6. 技术 RFC 草案与 unresolved-questions 边界案例
Clone-Shallow `
    "https://github.com/rust-lang/project-safe-transmute.git" `
    "rust-safe-transmute"

# 7. 可复现实验 recipe（仓库已归档）
Clone-Shallow `
    "https://github.com/yahoo/ml-reproducibility-guidelines.git" `
    "yahoo-ml-reproducibility"

# 8. Artifact evaluation checklist / submission / reviewing
# Clone-Sparse `
#     "https://github.com/ctuning/artifact-evaluation.git" `
#     "artifact-evaluation" `
#     @("docs", "LICENSE", "README.md")

# 9. 开发—测试—实验复合工作区和 benchmark report 文档
# Clone-Sparse `
#     "https://github.com/llm-d/llm-d-benchmark.git" `
#     "llm-d-benchmark" `
#     @(
#         "README.md",
#         "config/README.md",
#         "docs",
#         "llmdbenchmark/experiment/README.md",
#         "llmdbenchmark/analysis/benchmark_report/README.md",
#         "LICENSE"
#     )

# 10. 路线图候选，只作 seed，不直接作为 positive
Clone-Sparse `
    "https://github.com/nexu-io/open-design.git" `
    "open-design" `
    @("docs", "LICENSE", "README.md")

Set-Location $root