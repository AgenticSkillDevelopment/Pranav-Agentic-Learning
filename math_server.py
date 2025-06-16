from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    '''
    add 2 numbers
    '''
    return a+b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    '''
    multiply 2 numbers
    '''
    return a*b

#transport="stdio" tells the server 
# to use the standard input/output (stdin/stdout) to receive and respond to tool function calls




if __name__ == "__main__":
    mcp.run(transport="stdio")