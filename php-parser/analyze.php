
<?php

require __DIR__ . '/vendor/autoload.php';

use PhpParser\Error;
use PhpParser\Node;
use PhpParser\NodeFinder;
use PhpParser\ParserFactory;

if ($argc !== 2) {
    fwrite(STDERR, "Usage: php analyze.php <file.php>\n");
    exit(1);
}

$filePath = $argv[1];

if (!is_file($filePath)) {
    fwrite(STDERR, "File not found: {$filePath}\n");
    exit(1);
}

$code = file_get_contents($filePath);

$parser = (new ParserFactory())->createForNewestSupportedVersion();

try {
    $ast = $parser->parse($code);
} catch (Error $error) {
    fwrite(STDERR, "PHP parse error: {$error->getMessage()}\n");
    exit(1);
}


$finder = new NodeFinder();

$classes = [];
$functions = [];

$classNodes = $finder->findInstanceOf(
    $ast ?? [],
    Node\Stmt\Class_::class
);

foreach ($classNodes as $node) {
    $methods = [];

    foreach ($node->getMethods() as $method) {
        $methods[] = [
            'name' => $method->name->toString(),
            'line' => $method->getStartLine(),
            'visibility' => $method->isPublic()
                ? 'public'
                : ($method->isProtected() ? 'protected' : 'private'),
        ];
    }

    $classes[] = [
        'name' => $node->name?->toString(),
        'line' => $node->getStartLine(),
        'methods' => $methods,
    ];
}

$functionNodes = $finder->findInstanceOf(
    $ast ?? [],
    Node\Stmt\Function_::class
);

foreach ($functionNodes as $node) {
    $functions[] = [
        'name' => $node->name->toString(),
        'line' => $node->getStartLine(),
    ];
}

$result = [
    'file' => $filePath,
    'language' => 'php',
    'classes' => $classes,
    'functions' => $functions,
];


echo json_encode(
    $result,
    JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
) . PHP_EOL;
